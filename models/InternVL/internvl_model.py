"""
InternVL model wrapper using HuggingFace.
Supports InternVL2, InternVL2.5, and InternVL3 models via remote code.
"""

import logging
import os
import tempfile
import time

import torch
from PIL import Image

from models.base_model import BaseModel

logger = logging.getLogger("vlm_benchmark")


class InternVLModel(BaseModel):
    """Wrapper class for InternVL models."""

    def __init__(
        self,
        model_id: str = "OpenGVLab/InternVL2_5-8B",
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
        """Loads InternVL model using AutoModel and AutoTokenizer with trust_remote_code=True."""
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
                f"Loading InternVL model {self.model_id} on {self.device} with precision {torch_dtype}..."
            )

            # Load model & tokenizer
            self.processor = AutoTokenizer.from_pretrained(
                self.model_id, trust_remote_code=True, use_fast=False
            )

            self.model = AutoModel.from_pretrained(
                self.model_id,
                torch_dtype=torch_dtype,
                device_map=device_map,
                quantization_config=quantization_config,
                trust_remote_code=True,
            ).eval()

            self.is_loaded = True
            self.load_time = time.time() - start_time
            logger.info(f"InternVL model loaded successfully in {self.load_time:.2f}s.")

        except Exception as e:
            logger.error(f"Failed to load InternVL model: {e}")
            raise RuntimeError(f"InternVL load failed: {e}")

    def generate(self, image: Image.Image, prompt: str) -> str:
        """Runs InternVL prediction by saving image to temporary file and calling custom chat API."""
        if not self.is_loaded or self.model is None or self.processor is None:
            raise RuntimeError("InternVL model is not loaded. Call load() first.")

        temp_img_path = None
        try:
            import torch

            # Convert RGBA/P to RGB
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            # Create a temporary file to save the image
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                image.save(temp_file.name, format="JPEG")
                temp_img_path = temp_file.name

            # Load and preprocess using the model's remote implementation of load_image
            # Note: InternVL imports are usually exposed on the model or require import
            # If load_image is not directly importable, we can implement the core logic
            # or try to import it from the dynamic remote code modules.
            # Usually, we can use the model's internal pixel values logic.
            # InternVL's remote code usually exposes a load_image method or we can preprocess ourselves.
            try:
                # Try to import load_image from the dynamic module or use standard method
                # Often, we can inspect model config or import load_image.
                # Let's import from transformers' custom module if registered, or write the helper:
                # Standard InternVL load_image:
                # We can write a custom preprocessor to avoid import errors
                pixel_values = self._preprocess_image(image)
            except Exception as e:
                logger.warning(
                    f"Custom preprocessor failed: {e}. Attempting import from model..."
                )
                # Fallback: some InternVL versions expose it on the model namespace
                if hasattr(self.model, "load_image"):
                    pixel_values = self.model.load_image(temp_img_path)
                else:
                    raise e

            # Move pixel values to device/precision
            torch_dtype = (
                torch.bfloat16
                if self.precision == "bf16" and torch.cuda.is_bf16_supported()
                else torch.float16
            )
            if self.device == "cuda":
                pixel_values = pixel_values.to(torch_dtype).cuda()
            else:
                pixel_values = pixel_values.to(torch_dtype)

            # Build generation config
            generation_config = dict(max_new_tokens=1024, do_sample=False)

            question = f"<image>\n{prompt}"

            logger.info("Executing InternVL chat...")
            with torch.no_grad():
                response = self.model.chat(
                    self.processor, pixel_values, question, generation_config
                )

            return response.strip()

        except Exception as e:
            logger.error(f"Error during InternVL prediction: {e}")
            raise RuntimeError(f"InternVL prediction failed: {e}")
        finally:
            # Clean up the temporary image
            if temp_img_path and os.path.exists(temp_img_path):
                try:
                    os.remove(temp_img_path)
                except Exception:
                    pass

    def _preprocess_image(
        self, image: Image.Image, input_size: int = 448, max_num: int = 12
    ) -> torch.Tensor:
        """
        Custom image preprocessor matching InternVL's dynamic patching.
        Resizes and crops image into tiles to feed into the ViT encoder.
        """
        import torchvision.transforms as T

        # Define transforms
        IMAGENET_MEAN = (0.485, 0.456, 0.406)
        IMAGENET_STD = (0.229, 0.224, 0.225)

        transform = T.Compose(
            [T.ToTensor(), T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)]
        )

        # Dynamic patch splitting
        orig_w, orig_h = image.size
        aspect_ratio = orig_w / orig_h

        # Find best tile grid
        best_grid = (1, 1)
        min_diff = float("inf")

        for r in range(1, max_num + 1):
            for c in range(1, max_num + 1):
                if r * c <= max_num:
                    grid_aspect = c / r
                    diff = abs(aspect_ratio - grid_aspect)
                    if diff < min_diff:
                        min_diff = diff
                        best_grid = (r, c)

        rows, cols = best_grid
        target_w = cols * input_size
        target_h = rows * input_size

        # Resize image to fit the grid
        resized_img = image.resize((target_w, target_h), Image.Resampling.BILINEAR)

        # Extract patches
        patches = []
        for r in range(rows):
            for c in range(cols):
                box = (
                    c * input_size,
                    r * input_size,
                    (c + 1) * input_size,
                    (r + 1) * input_size,
                )
                patch = resized_img.crop(box)
                patches.append(transform(patch))

        # Also append a thumbnail (resized original)
        thumbnail = image.resize((input_size, input_size), Image.Resampling.BILINEAR)
        patches.append(transform(thumbnail))

        # Stack into [N, C, H, W]
        return torch.stack(patches)
