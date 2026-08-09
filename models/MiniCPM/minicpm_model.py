"""
MiniCPM-V model wrapper using HuggingFace.
Supports MiniCPM-Llama3-V-2_5 and MiniCPM-V-2_6 via remote code.
"""

import logging
import time

from PIL import Image

from models.base_model import BaseModel

logger = logging.getLogger("vlm_benchmark")


class MiniCPMModel(BaseModel):
    """Wrapper class for MiniCPM-V models."""

    def __init__(
        self,
        model_id: str = "openbmb/MiniCPM-Llama3-V-2_5",
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
        self.tokenizer = None

    def load_model(self) -> None:
        """Loads MiniCPM model using AutoModel and AutoTokenizer with trust_remote_code=True."""
        start_time = time.time()

        try:
            import torch
            from transformers import AutoModel, AutoTokenizer

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
                f"Loading MiniCPM model {self.model_id} on {self.device} with precision {torch_dtype}..."
            )

            # Load model & tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_id, trust_remote_code=True
            )

            self.model = AutoModel.from_pretrained(
                self.model_id,
                torch_dtype=torch_dtype,
                device_map=device_map,
                quantization_config=quantization_config,
                trust_remote_code=True,
            ).eval()

            self.processor = self.tokenizer  # Set standard processor alias
            self.is_loaded = True
            self.load_time = time.time() - start_time
            logger.info(f"MiniCPM model loaded successfully in {self.load_time:.2f}s.")

        except Exception as e:
            logger.error(f"Failed to load MiniCPM model: {e}")
            raise RuntimeError(f"MiniCPM load failed: {e}")

    def generate(self, image: Image.Image, prompt: str) -> str:
        """Runs MiniCPM-V inference using model's chat template."""
        if not self.is_loaded or self.model is None or self.tokenizer is None:
            raise RuntimeError("MiniCPM model is not loaded. Call load() first.")

        try:
            import torch

            # Convert RGBA/P to RGB
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            # Setup user messages format
            msgs = [{"role": "user", "content": [image, prompt]}]

            logger.info("Executing MiniCPM chat...")
            with torch.no_grad():
                # MiniCPM chat accepts msgs directly
                response = self.model.chat(
                    image=None,
                    msgs=msgs,
                    tokenizer=self.tokenizer,
                    sampling=False,  # arg for greedy search
                    max_new_tokens=1024,
                )

            return response.strip()

        except Exception as e:
            logger.error(f"Error during MiniCPM prediction: {e}")
            raise RuntimeError(f"MiniCPM prediction failed: {e}")

    def cleanup(self) -> None:
        """Cleans up MiniCPM tokenizer."""
        self.tokenizer = None
        super().unload()
