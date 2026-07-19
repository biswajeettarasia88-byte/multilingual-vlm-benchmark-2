"""
Llama-3.2 Vision model wrapper using HuggingFace.
Loads checkpoint and performs inference using MllamaForConditionalGeneration.
"""

import logging
import time

from PIL import Image

from project.models.base_model import BaseModel

logger = logging.getLogger("vlm_benchmark")


class LlamaModel(BaseModel):
    """Wrapper class for Llama-3.2 Vision models."""

    def __init__(
        self,
        model_id: str = "meta-llama/Llama-3.2-11B-Vision-Instruct",
        device: str = "cuda",
        precision: str = "bf16",
        quantization: str = "4bit",
        **kwargs,
    ):
        super().__init__(
            model_id=model_id,
            device=device,
            precision=precision,
            quantization=quantization,
            **kwargs,
        )

    def load_model(self) -> None:
        """Loads Llama-3.2 model using AutoProcessor and MllamaForConditionalGeneration."""
        start_time = time.time()

        try:
            import torch
            from transformers import AutoProcessor, MllamaForConditionalGeneration

            # Determine torch data type
            if (
                self.precision == "bf16"
                and torch.cuda.is_available()
                and torch.cuda.is_bf16_supported()
            ):
                torch_dtype = torch.bfloat16
            elif self.precision == "fp16" and torch.cuda.is_available():
                torch_dtype = torch.float16
            else:
                torch_dtype = torch.float32

            # Configure Quantization
            quantization_config = None
            device_map = None

            if self.device == "cuda" and torch.cuda.is_available():
                device_map = "auto"
                if self.quantization == "4bit":
                    from transformers import BitsAndBytesConfig

                    quantization_config = BitsAndBytesConfig(
                        load_in_4bit=True,
                        bnb_4bit_compute_dtype=torch_dtype,
                        bnb_4bit_quant_type="nf4",
                        bnb_4bit_use_double_quant=True,
                    )
                elif self.quantization == "8bit":
                    from transformers import BitsAndBytesConfig

                    quantization_config = BitsAndBytesConfig(load_in_8bit=True)
            else:
                self.device = "cpu"
                device_map = {"": "cpu"}

            logger.info(
                f"Loading Llama Vision model {self.model_id} on {self.device} with precision {torch_dtype}..."
            )

            # Load model & processor
            self.processor = AutoProcessor.from_pretrained(self.model_id)
            self.model = MllamaForConditionalGeneration.from_pretrained(
                self.model_id,
                torch_dtype=torch_dtype,
                device_map=device_map,
                quantization_config=quantization_config,
                trust_remote_code=self.kwargs.get("trust_remote_code", True),
            )

            self.is_loaded = True
            self.load_time = time.time() - start_time
            logger.info(f"Llama model loaded successfully in {self.load_time:.2f}s.")

        except Exception as e:
            logger.error(f"Failed to load Llama model: {e}")
            raise RuntimeError(f"Llama load failed: {e}")

    def generate(self, image: Image.Image, prompt: str) -> str:
        """Runs Llama-3.2 Vision prediction using chat template."""
        if not self.is_loaded or self.model is None or self.processor is None:
            raise RuntimeError("Llama model is not loaded. Call load() first.")

        try:
            import torch

            # Convert RGBA/P to RGB
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            # Setup conversational inputs with image placeholder
            messages = [
                {
                    "role": "user",
                    "content": [{"type": "image"}, {"type": "text", "text": prompt}],
                }
            ]

            # Apply Llama's specific chat template
            input_text = self.processor.apply_chat_template(
                messages, add_generation_prompt=True
            )

            inputs = self.processor(
                image, input_text, add_special_tokens=False, return_tensors="pt"
            )

            # Move inputs to target device
            if self.quantization == "none" or self.device == "cpu":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            else:
                inputs = {k: v.to("cuda") for k, v in inputs.items()}

            logger.info("Executing Llama generation...")
            with torch.no_grad():
                output_ids = self.model.generate(**inputs, max_new_tokens=1024)

            # Decode output, removing original prompt tokens
            prompt_len = inputs["input_ids"].shape[1]
            generated_ids = output_ids[0][prompt_len:]

            response = self.processor.decode(generated_ids, skip_special_tokens=True)

            return response.strip()

        except Exception as e:
            logger.error(f"Error during Llama prediction: {e}")
            raise RuntimeError(f"Llama prediction failed: {e}")
