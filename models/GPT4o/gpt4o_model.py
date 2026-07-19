"""
GPT-4o model wrapper using the OpenAI API.
Encodes PIL images as base64 and queries the gpt-4o chat completions endpoint.
"""

import base64
import logging
import os
import time
from io import BytesIO
from typing import Optional

from PIL import Image

from project.models.base_model import BaseModel

logger = logging.getLogger("vlm_benchmark")


class GPT4oModel(BaseModel):
    """Wrapper class for OpenAI's GPT-4o model."""

    def __init__(self, model_id: str = "gpt-4o", device: str = "cpu", **kwargs):
        # API models run on the cloud, so device defaults to cpu
        kwargs.pop("precision", None)
        kwargs.pop("quantization", None)
        super().__init__(
            model_id=model_id,
            device=device,
            precision="none",
            quantization="none",
            **kwargs,
        )
        self.client = None
        self.api_key: Optional[str] = None

    def load_model(self) -> None:
        """Initializes the OpenAI client using environment variables."""
        start_time = time.time()
        api_key_env = self.kwargs.get("api_key_env", "OPENAI_API_KEY")
        self.api_key = os.getenv(api_key_env)

        if not self.api_key:
            raise ValueError(
                f"API key environment variable '{api_key_env}' is not set. Cannot load GPT-4o."
            )

        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=self.api_key)
            self.is_loaded = True
            self.load_time = time.time() - start_time
            logger.info(
                f"GPT-4o client initialized successfully in {self.load_time:.2f}s."
            )
        except ImportError:
            raise ImportError(
                "The 'openai' library is required to run GPT-4o. Please install it using pip."
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OpenAI client: {e}")

    def generate(self, image: Image.Image, prompt: str) -> str:
        """Encodes image to base64 and runs inference via the ChatCompletions API."""
        if not self.is_loaded or self.client is None:
            raise RuntimeError("GPT-4o model is not loaded. Call load() first.")

        try:
            # Convert PIL image to base64 JPEG bytes
            buffered = BytesIO()
            # Convert RGBA/P to RGB to ensure JPEG compatibility
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            image.save(buffered, format="JPEG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # Construct the messages payload
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"},
                        },
                    ],
                }
            ]

            # API Request
            logger.info("Sending request to GPT-4o API...")
            temperature = self.kwargs.get("temperature", 0.0)
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                response_format={"type": "json_object"} if "JSON" in prompt else None,
                temperature=temperature,
                max_tokens=2048,
            )

            output_text = response.choices[0].message.content
            if not output_text:
                raise ValueError("Empty response received from GPT-4o API.")

            return output_text.strip()

        except Exception as e:
            logger.error(f"Error during GPT-4o prediction: {e}")
            raise RuntimeError(f"GPT-4o prediction failed: {e}")

    def cleanup(self) -> None:
        """Nullifies API client reference."""
        self.client = None
        super().cleanup()
