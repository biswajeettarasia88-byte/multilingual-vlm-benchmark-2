import unittest
from PIL import Image
from models import get_model, MODEL_REGISTRY
from models.base_model import BaseModel

class TestVLMModels(unittest.TestCase):
    def test_model_registry(self):
        self.assertIn("qwen", MODEL_REGISTRY)
        self.assertIn("gemini", MODEL_REGISTRY)
        
    def test_factory_invalid_model(self):
        with self.assertRaises(ValueError):
            get_model("invalid_model_name")
            
    def test_model_wrapper_initialization(self):
        model = get_model("gpt4o", api_key_env="DUMMY_KEY")
        self.assertIsInstance(model, BaseModel)
        
    def test_unloaded_generate_raises_error(self):
        model = get_model("gpt4o", api_key_env="DUMMY_KEY")
        img = Image.new("RGB", (10, 10), color="blue")
        with self.assertRaises(RuntimeError):
            model.generate(img, "test prompt")
