"""
Qwen2.5-VL-7B model wrapper using HuggingFace transformers.
Loads local checkpoints and runs inference on CUDA/CPU.
"""

import logging
import time

from PIL import Image

from models.base_model import BaseModel

logger = logging.getLogger("vlm_benchmark")


class QwenModel(BaseModel):
    """Wrapper class for Qwen2.5-VL-7B model."""

    def __init__(
        self,
        model_id: str = "Qwen/Qwen2.5-VL-7B-Instruct",
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
        """Loads Qwen2.5-VL model using AutoProcessor and Qwen2_5_VLForConditionalGeneration."""
        start_time = time.time()

        try:
            import torch
            from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration

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
                f"Loading Qwen model {self.model_id} on {self.device} with precision {torch_dtype}..."
            )

            # Load model & processor
            self.processor = AutoProcessor.from_pretrained(self.model_id)
            self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                self.model_id,
                torch_dtype=torch_dtype,
                device_map=device_map,
                quantization_config=quantization_config,
                trust_remote_code=self.kwargs.get("trust_remote_code", True),
            )

            self.is_loaded = True
            self.load_time = time.time() - start_time
            logger.info(f"Qwen model loaded successfully in {self.load_time:.2f}s.")

        except Exception as e:
            logger.error(f"Failed to load Qwen model: {e}")
            raise RuntimeError(f"Qwen load failed: {e}")

    def generate(self, image: Image.Image, prompt: str) -> str:
        """Runs Qwen2.5-VL prediction using official utilities."""
        if not self.is_loaded or self.model is None or self.processor is None:
            raise RuntimeError("Qwen model is not loaded. Call load() first.")

        try:
            import torch
            from qwen_vl_utils import process_vision_info

            # Format image & text
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": prompt},
                    ],
                }
            ]

            # Prep inputs
            text = self.processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            image_inputs, video_inputs = process_vision_info(messages)

            inputs = self.processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt",
            )

            # Move inputs to target device (or let device_map handle it)
            if self.quantization == "none" or self.device == "cpu":
                inputs = inputs.to(self.device)
            else:
                # When using bitsandbytes device_map='auto', it's best to move active tensors to CUDA
                inputs = inputs.to("cuda")

            with torch.no_grad():
                generated_ids = self.model.generate(**inputs, max_new_tokens=1024)

            generated_ids_trimmed = [
                out_ids[len(in_ids) :]
                for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]

            output_text = self.processor.batch_decode(
                generated_ids_trimmed,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )

            return output_text[0].strip()

        except Exception as e:
            logger.error(f"Error during Qwen prediction: {e}")
            raise RuntimeError(f"Qwen prediction failed: {e}")
