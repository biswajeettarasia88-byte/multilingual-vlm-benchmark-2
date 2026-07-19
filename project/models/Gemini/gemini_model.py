"""
Gemini model wrapper using the Google Generative AI API.
Queries the gemini-2.5-flash model with a PIL image and text prompt.
"""

import logging
import os
import time
from typing import Optional

from PIL import Image

from project.models.base_model import BaseModel

logger = logging.getLogger("vlm_benchmark")


class GeminiModel(BaseModel):
    """Wrapper class for Google's Gemini model."""

    def __init__(
        self, model_id: str = "gemini-2.5-flash", device: str = "cpu", **kwargs
    ):
        kwargs.pop("precision", None)
        kwargs.pop("quantization", None)
        super().__init__(
            model_id=model_id,
            device=device,
            precision="none",
            quantization="none",
            **kwargs,
        )
        self.api_key: Optional[str] = None
        self.model_client = None

    def load_model(self) -> None:
        """Initializes the GenerativeModel client using environment variables."""
        start_time = time.time()
        api_key_env = self.kwargs.get("api_key_env", "GEMINI_API_KEY")
        self.api_key = os.getenv(api_key_env)

        if not self.api_key:
            raise ValueError(
                f"API key environment variable '{api_key_env}' is not set. Cannot load Gemini."
            )

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            self.model_client = genai.GenerativeModel(self.model_id)
            self.is_loaded = True
            self.load_time = time.time() - start_time
            logger.info(
                f"Gemini client initialized successfully in {self.load_time:.2f}s."
            )
        except ImportError:
            raise ImportError(
                "The 'google-generativeai' library is required to run Gemini. Please install it using pip."
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini client: {e}")

    def generate(self, image: Image.Image, prompt: str) -> str:
        """Runs Gemini inference using the SDK."""
        if not self.is_loaded or self.model_client is None:
            raise RuntimeError("Gemini model is not loaded. Call load() first.")

        try:
            # Force RGB conversion if image has an alpha channel or is palette-based
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            # Setup generation configuration to force JSON if specified
            import google.generativeai as genai

            config = {}
            if "JSON" in prompt:
                config["response_mime_type"] = "application/json"

            temperature = self.kwargs.get("temperature", 0.0)
            config["temperature"] = temperature

            logger.info("Sending request to Gemini API...")
            response = self.model_client.generate_content(
                contents=[image, prompt],
                generation_config=genai.types.GenerationConfig(**config),
            )

            output_text = response.text
            if not output_text:
                raise ValueError("Empty response received from Gemini API.")

            return output_text.strip()

        except Exception as e:
            logger.error(f"Error during Gemini prediction: {e}")
            raise RuntimeError(f"Gemini prediction failed: {e}")

    def cleanup(self) -> None:
        """Nullifies API client reference."""
        self.model_client = None
        super().cleanup()
