import json
import logging
from PIL import Image
from project.models.base_model import BaseModel

logger = logging.getLogger("vlm_benchmark")

class MockModel(BaseModel):
    def __init__(self, model_id: str = "mock-model", device: str = "cpu", **kwargs):
        kwargs.pop("precision", None)
        kwargs.pop("quantization", None)
        super().__init__(
            model_id=model_id,
            device=device,
            precision="none",
            quantization="none",
            **kwargs,
        )

    def load_model(self) -> None:
        self.is_loaded = True
        self.load_time = 0.1
        logger.info("Mock model loaded.")

    def generate(self, image: Image.Image, prompt: str) -> str:
        if not self.is_loaded:
            raise RuntimeError("Mock model not loaded.")
        
        # Simple JSON response for Task 2
        response = {
            "ocr_text": "MOCK TEXT",
            "scripts": ["Latin"],
            "languages": ["English"],
            "multilingual_extraction": {
                "original": "MOCK TEXT",
                "romanized": "MOCK TEXT",
                "english_translation": "MOCK TEXT"
            },
            "text_qa": {
                "Q": "What does the text say?",
                "A": "MOCK TEXT"
            }
        }
        return json.dumps(response)

    def cleanup(self) -> None:
        super().cleanup()
