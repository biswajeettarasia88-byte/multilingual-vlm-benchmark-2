"""
Benchmark orchestrator for loading, running, profiling, and unloading VLMs.
Manages smart resume, GPU OOM recovery, warm-up, and detailed logging.
"""

import csv
import gc
import json
import logging
import time
from typing import List, Optional

import torch
from tqdm import tqdm

from project.config import BenchmarkConfig
from project.loader import DatasetLoader, VLMDataset
from project.models import get_model
from project.utils import (
    get_peak_gpu_memory_gb,
    log_gpu_metric,
    parse_and_clean_json,
    reset_peak_gpu_memory,
)

logger = logging.getLogger("vlm_benchmark")


class BenchmarkEngine:
    """BenchmarkEngine executes the VLM comparison suite on the loaded dataset."""

    def __init__(self, config: BenchmarkConfig, loader: DatasetLoader):
        self.config = config
        self.loader = loader
        self.output_root = config.get_path("paths.output_root", "Outputs")
        self.logs_root = config.get_path("paths.evaluation_root", "Evaluation") / "Logs"
        self.logs_root.mkdir(parents=True, exist_ok=True)

        # Load prompt
        self.prompt_path = config.get_path(
            "prompt.prompt_file", "prompts/benchmark_prompt.txt"
        )
        self.prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        """Reads the standard benchmark prompt from the configured file."""
        if not self.prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found at {self.prompt_path}")
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
        logger.info(f"Loaded benchmark prompt ({len(prompt)} chars).")
        return prompt

    def run_all(self, max_images: Optional[int] = None) -> List[str]:
        """Runs the entire enabled model benchmark suite."""
        enabled_models = []
        models_config = self.config.get("models", {})

        for m_key, m_val in models_config.items():
            if m_val.get("enabled", False):
                enabled_models.append(m_key)

        logger.info(f"Models queued for benchmarking: {enabled_models}")
        print(f"Queued models: {enabled_models}\n")

        dataset = VLMDataset(self.loader, max_records=max_images)
        if len(dataset) == 0:
            logger.error("Dataset contains 0 valid images. Benchmarking aborted.")
            print("Error: No images found to process!")
            return []

        completed_models = []
        for model_key in enabled_models:
            print(f"\n==================================================")
            print(f"RUNNING BENCHMARK FOR MODEL: {model_key.upper()}")
            print(f"==================================================")

            try:
                success = self.run_model(model_key, dataset)
                if success:
                    completed_models.append(model_key)
            except Exception as e:
                logger.error(
                    f"Critical failure benchmarking model {model_key}: {e}",
                    exc_info=True,
                )
                print(f"Failed to benchmark model {model_key}: {e}")

        return completed_models

    def run_model(self, model_key: str, dataset: VLMDataset) -> bool:
        """Runs the benchmark pipeline for a single model."""
        m_cfg = self.config.get(f"models.{model_key}", {})
        model_id = m_cfg.get("model_id", m_cfg.get("model_name"))

        # Setup paths
        model_output_dir = self.output_root / model_key.capitalize()
        model_output_dir.mkdir(parents=True, exist_ok=True)
        csv_log_path = self.logs_root / f"{model_key}_benchmark.csv"

        # Open CSV log file
        csv_exists = csv_log_path.exists()
        csv_file = open(csv_log_path, "a", newline="", encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        if not csv_exists:
            csv_writer.writerow(
                [
                    "image_id",
                    "status",
                    "inference_time_sec",
                    "peak_gpu_mem_gb",
                    "load_time_sec",
                    "precision",
                    "quantization",
                    "error_message",
                ]
            )

        # Resolve loading configurations
        device = self.config.get("runtime.device", "cuda")
        precision = self.config.get("runtime.default_precision", "bf16")
        quantization = self.config.get("runtime.quantization", "4bit")

        # Loading logic with dynamic retry if CUDA OOM occurs
        model_wrapper = None
        load_attempts = [
            (precision, quantization, device),
            (precision, "8bit", device),
            (precision, "4bit", device),
            ("fp16", "4bit", device),
            ("float32", "none", "cpu"),  # CPU Fallback
        ]

        # Filter duplicates in load_attempts
        seen_attempts = set()
        unique_attempts = []
        for att in load_attempts:
            # If CUDA is unavailable, force CPU
            att_device = "cpu" if not torch.cuda.is_available() else att[2]
            att_quant = "none" if att_device == "cpu" else att[1]
            tup = (att[0], att_quant, att_device)
            if tup not in seen_attempts:
                seen_attempts.add(tup)
                unique_attempts.append(tup)

        loaded = False
        load_time = 0.0

        for idx, (p, q, d) in enumerate(unique_attempts):
            logger.info(
                f"Attempting to load {model_key} with precision={p}, quantization={q}, device={d}..."
            )
            print(
                f"Loading model (Attempt {idx+1}/{len(unique_attempts)}: precision={p}, quantization={q}, device={d})..."
            )

            try:
                # Force clean memory before loading
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

                m_cfg_copy = m_cfg.copy()
                m_cfg_copy.pop("model_name", None)
                model_wrapper = get_model(
                    model_key,
                    model_id=model_id,
                    device=d,
                    precision=p,
                    quantization=q,
                    **m_cfg_copy,
                )

                model_wrapper.load_model()
                load_time = model_wrapper.load_time
                precision, quantization, device = p, q, d
                loaded = True
                print(f"Model loaded successfully in {load_time:.2f}s!")
                break
            except Exception as e:
                err_msg = str(e)
                logger.warning(f"Failed loading wrapper (Attempt {idx+1}): {err_msg}")
                if "CUDA out of memory" in err_msg or "OOM" in err_msg:
                    log_gpu_metric(
                        self.logs_root.parent,
                        f"CUDA OOM loading {model_key} at {p}/{q}. Retrying lower settings...",
                    )
                if idx == len(unique_attempts) - 1:
                    logger.error(f"All load attempts failed for model {model_key}")
                    print(
                        f"Error: Could not load {model_key} after {len(unique_attempts)} attempts."
                    )
                    csv_writer.writerow(["ALL", "FAILED_LOAD", 0, 0, 0, p, q, err_msg])
                    csv_file.close()
                    return False

        if not loaded or model_wrapper is None:
            csv_file.close()
            return False

        # Run model Warm-Up (Step 5)
        print("Running model warm-up...")
        try:
            # Use the first image in dataset for warm-up
            warmup_img, _, _, _ = dataset[0]
            # Warm up with a simple prompt
            _ = model_wrapper.generate(
                warmup_img, "Warm up. Identify any text: Hello World"
            )
            logger.info("Model warm-up completed successfully.")
        except Exception as e:
            logger.warning(f"Model warm-up failed (non-fatal): {e}")

        # Core inference loop over all images
        resume = self.config.get("runtime.resume", True)

        for idx in tqdm(range(len(dataset)), desc=f"Benchmarking {model_key}"):
            # Lazily load image
            try:
                image, image_id, metadata, original_json = dataset[idx]
            except Exception as e:
                logger.error(f"Failed to load image index {idx}: {e}")
                csv_writer.writerow(
                    [
                        f"idx_{idx}",
                        "FAILED_LOAD_IMAGE",
                        0,
                        0,
                        0,
                        precision,
                        quantization,
                        str(e),
                    ]
                )
                continue

            # Target JSON and raw text files
            output_json_path = model_output_dir / f"{image_id}.json"
            output_raw_path = model_output_dir / f"{image_id}_raw.txt"

            # Check resume (Step 5/10)
            if resume and output_json_path.exists() and output_raw_path.exists():
                logger.info(f"Skipping {image_id} for {model_key} (already processed).")
                continue

            # Run prediction
            reset_peak_gpu_memory()
            start_inference = time.time()

            status = "SUCCESS"
            error_message = ""
            raw_output = ""
            parsed_data = {}
            inference_time = 0.0
            peak_gpu_mem = 0.0

            try:
                # Core inference
                raw_output = model_wrapper.generate(image, self.prompt)
                inference_time = time.time() - start_inference
                peak_gpu_mem = get_peak_gpu_memory_gb()

                # Clean & parse JSON
                parsed_data = parse_and_clean_json(raw_output)
            except Exception as e:
                inference_time = time.time() - start_inference
                peak_gpu_mem = get_peak_gpu_memory_gb()
                err_str = str(e)

                # Check for OOM during prediction
                if "CUDA out of memory" in err_str:
                    status = "OOM_FAILURE"
                    error_message = "CUDA Out of Memory during inference."
                    log_gpu_metric(
                        self.logs_root.parent,
                        f"CUDA OOM on inference for {model_key}, Image ID: {image_id}",
                    )
                else:
                    status = "INFERENCE_FAILURE"
                    error_message = err_str

                logger.error(
                    f"Prediction failed for image {image_id} on {model_key}: {e}"
                )
                parsed_data = {
                    "error": status,
                    "message": error_message,
                    "ocr_text": "",
                    "scripts": [],
                    "languages": [],
                    "multilingual_extraction": {
                        "original": "",
                        "romanized": "",
                        "english_translation": "",
                    },
                    "text_qa": {},
                }

            # Save raw model generation
            try:
                with open(output_raw_path, "w", encoding="utf-8") as f:
                    f.write(raw_output)
            except Exception as e:
                logger.error(f"Failed to save raw output for {image_id}: {e}")

            # Save parsed/structured JSON output (Step 9)
            structured_data = {
                "image_id": image_id,
                "model_id": model_id,
                "model_version": getattr(model_wrapper, "version", "1.0"),
                "gpu_used": (
                    torch.cuda.get_device_name(0)
                    if torch.cuda.is_available()
                    else "None (CPU)"
                ),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "processing_time_sec": round(inference_time, 4),
                "peak_gpu_mem_gb": round(peak_gpu_mem, 4),
                "prompt": self.prompt,
                # Model generated fields
                "ocr_text": parsed_data.get("ocr_text", ""),
                "scripts": parsed_data.get("scripts", []),
                "languages": parsed_data.get("languages", []),
                "multilingual_extraction": parsed_data.get(
                    "multilingual_extraction", {}
                ),
                "text_qa": parsed_data.get("text_qa", {}),
            }

            try:
                with open(output_json_path, "w", encoding="utf-8") as f:
                    json.dump(structured_data, f, indent=2)
            except Exception as e:
                logger.error(f"Failed to save structured JSON for {image_id}: {e}")

            # Log to CSV
            csv_writer.writerow(
                [
                    image_id,
                    status,
                    round(inference_time, 4),
                    round(peak_gpu_mem, 4),
                    round(load_time, 4),
                    precision,
                    quantization,
                    error_message,
                ]
            )
            csv_file.flush()  # Force flush to disk to preserve resume logs

        csv_file.close()

        # Unload model and free memory (Step 5)
        model_wrapper.cleanup()
        del model_wrapper
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        print(f"Finished benchmark for {model_key}.\n")
        return True
