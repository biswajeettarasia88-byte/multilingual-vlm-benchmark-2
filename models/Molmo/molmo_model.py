"""
Molmo model wrapper using HuggingFace.
Loads AllenAI Molmo-7B checkpoints and runs inference.
"""

import logging
import time

from PIL import Image

from models.base_model import BaseModel

logger = logging.getLogger("vlm_benchmark")


class MolmoModel(BaseModel):
    """Wrapper class for Molmo models."""

    def __init__(
        self,
        model_id: str = "allenai/Molmo-7B-D-0924",
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
        """Loads Molmo model using AutoModelForCausalLM and AutoProcessor with trust_remote_code=True."""
        start_time = time.time()

        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoProcessor

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
                f"Loading Molmo model {self.model_id} on {self.device} with precision {torch_dtype}..."
            )

            # Load processor and model
            self.processor = AutoProcessor.from_pretrained(
                self.model_id, trust_remote_code=True
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=torch_dtype,
                device_map=device_map,
                quantization_config=quantization_config,
                trust_remote_code=True,
            ).eval()

            self.is_loaded = True
            self.load_time = time.time() - start_time
            logger.info(f"Molmo model loaded successfully in {self.load_time:.2f}s.")

        except Exception as e:
            logger.error(f"Failed to load Molmo model: {e}")
            raise RuntimeError(f"Molmo load failed: {e}")

    def generate(self, image: Image.Image, prompt: str) -> str:
        """Runs Molmo prediction using the custom generate_from_batch API."""
        if not self.is_loaded or self.model is None or self.processor is None:
            raise RuntimeError("Molmo model is not loaded. Call load() first.")

        try:
            import torch
            from transformers import GenerationConfig

            # Convert RGBA/P to RGB
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            # Process prompt & image
            inputs = self.processor.process(images=[image], text=prompt)

            # Move inputs to target device (or let device_map handle it)
            if self.quantization == "none" or self.device == "cpu":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            else:
                inputs = {k: v.to("cuda") for k, v in inputs.items()}

            # Add batch dimension to inputs if missing (processor.process usually adds it)
            logger.info("Executing Molmo generation...")

            with torch.no_grad():
                # Use Molmo's custom inference method which handles multimodal masks automatically
                outputs = self.model.generate_from_batch(
                    inputs,
                    GenerationConfig(
                        max_new_tokens=1024, stop_strings=["<|endoftext|>"]
                    ),
                    tokenizer=self.processor.tokenizer,
                )

            # Decode generated output, skipping the input prompt tokens
            input_len = inputs["input_ids"].shape[-1]
            generated_tokens = outputs[0, input_len:]

            response = self.processor.tokenizer.decode(
                generated_tokens, skip_special_tokens=True
            )

            return response.strip()

        except Exception as e:
            logger.error(f"Error during Molmo prediction: {e}")
            raise RuntimeError(f"Molmo prediction failed: {e}")


stream = None
