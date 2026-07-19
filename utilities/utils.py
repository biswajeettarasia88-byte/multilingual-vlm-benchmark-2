"""
Utility functions for logging, GPU memory tracking, system diagnostics, and JSON cleanup.
Provides helpers for reproducibility and robust error boundary control.
"""

import json
import logging
import platform
import sys
import time
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger("vlm_benchmark")


def setup_logging(logs_root: Path) -> None:
    """Sets up separate log files for benchmark, errors, and GPU tracking."""
    logs_root.mkdir(parents=True, exist_ok=True)

    # Root logger config
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Clear existing handlers
    root_logger.handlers = []

    # Formatting
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # General Benchmark Log File
    benchmark_handler = logging.FileHandler(
        logs_root / "benchmark.log", encoding="utf-8"
    )
    benchmark_handler.setLevel(logging.INFO)
    benchmark_handler.setFormatter(formatter)
    root_logger.addHandler(benchmark_handler)

    # Error Log File
    error_handler = logging.FileHandler(logs_root / "errors.log", encoding="utf-8")
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)

    logger.info("Logging initialized successfully.")


def log_gpu_metric(logs_root: Path, message: str) -> None:
    """Appends a VRAM or GPU specific event to gpu.log."""
    gpu_log_path = logs_root / "gpu.log"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(gpu_log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        logger.error(f"Failed to write to GPU log: {e}")


def get_system_info(output_path: Path) -> Dict[str, Any]:
    """Collects OS and CUDA environment specs, saving them to system_info.json."""
    sys_info: Dict[str, Any] = {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": sys.version.split()[0],
        "device_name": "CPU",
        "cuda_available": False,
        "cuda_version": "N/A",
        "gpu_count": 0,
        "gpu_details": [],
        "torch_version": "N/A",
        "transformers_version": "N/A",
    }

    # PyTorch and CUDA info
    try:
        import torch

        sys_info["torch_version"] = torch.__version__
        sys_info["cuda_available"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            sys_info["cuda_version"] = torch.version.cuda
            sys_info["gpu_count"] = torch.cuda.device_count()
            for i in range(torch.cuda.device_count()):
                name = torch.cuda.get_device_name(i)
                properties = torch.cuda.get_device_properties(i)
                total_mem_gb = properties.total_memory / (1024**3)
                sys_info["gpu_details"].append(
                    {"id": i, "name": name, "total_memory_gb": round(total_mem_gb, 2)}
                )
            sys_info["device_name"] = torch.cuda.get_device_name(0)
    except ImportError:
        pass

    # Transformers version
    try:
        import transformers

        sys_info["transformers_version"] = transformers.__version__
    except ImportError:
        pass

    # Save to JSON
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(sys_info, f, indent=2)
        logger.info(f"System specs logged to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save system info: {e}")

    return sys_info


def get_peak_gpu_memory_gb() -> float:
    """Returns the peak CUDA memory allocated in Gigabytes since the last reset."""
    try:
        import torch

        if torch.cuda.is_available():
            peak_bytes = torch.cuda.max_memory_allocated()
            return peak_bytes / (1024**3)
    except Exception:
        pass
    return 0.0


def reset_peak_gpu_memory() -> None:
    """Resets the peak CUDA memory allocation tracker."""
    try:
        import torch

        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
    except Exception:
        pass


def parse_and_clean_json(raw_text: str) -> Dict[str, Any]:
    """
    Cleans up VLM outputs, stripping markdown codeblocks and conversational padding,
    then parses the result as JSON.
    """
    text = raw_text.strip()

    # 1. Strip markdown wrapper (e.g. ```json ... ``` or ``` ...)
    if text.startswith("```"):
        # Find ending markdown
        lines = text.split("\n")
        # Remove first line if it starts with ```
        if lines[0].startswith("```"):
            lines = lines[1:]
        # Remove last line if it ends with ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    # 2. If it still doesn't parse, search for the first '{' and last '}'
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start_idx = text.find("{")
        end_idx = text.rfind("}")
        if start_idx != -1 and end_idx != -1:
            snippet = text[start_idx : end_idx + 1]
            try:
                return json.loads(snippet)
            except json.JSONDecodeError as e:
                logger.warning(f"Substring extraction failed to parse JSON: {e}")

        # Re-raise standard JSON exception if all recovery fails
        raise ValueError("Model output did not contain parseable JSON structure.")
