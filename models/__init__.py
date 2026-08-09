"""
Model registration and factory module for VLM benchmarking.
Allows dynamic loading of VLM classes by name.
"""

import logging
from typing import Dict, Type

from models.base_model import BaseModel
from models.Gemini.gemini_model import GeminiModel
from models.GPT4o.gpt4o_model import GPT4oModel
from models.InternVL.internvl_model import InternVLModel
from models.Llama.llama_model import LlamaModel
from models.MiniCPM.minicpm_model import MiniCPMModel
from models.Molmo.molmo_model import MolmoModel
from models.Phi4.phi4_model import Phi4Model
from models.Qwen.qwen_model import QwenModel

from models.Mock.mock_model import MockModel

logger = logging.getLogger("vlm_benchmark")

# Model Registry
MODEL_REGISTRY: Dict[str, Type[BaseModel]] = {
    "mock": MockModel,
    "gpt4o": GPT4oModel,
    "gemini": GeminiModel,
    "qwen": QwenModel,
    "internvl": InternVLModel,
    "minicpm": MiniCPMModel,
    "llama": LlamaModel,
    "molmo": MolmoModel,
    "phi4": Phi4Model,
}


def get_model(model_name: str, **kwargs) -> BaseModel:
    """
    Factory function to initialize a model wrapper from the registry.

    Args:
        model_name: String identifier (e.g., 'gpt4o', 'qwen', etc.).
        **kwargs: Configuration options passed to the model constructor.

    Returns:
        An instance of BaseModel.
    """
    model_name_clean = model_name.lower().replace("-", "").replace("_", "")

    if model_name_clean not in MODEL_REGISTRY:
        available = list(MODEL_REGISTRY.keys())
        raise ValueError(
            f"Unknown model name '{model_name}'. Available registered models: {available}"
        )

    model_class = MODEL_REGISTRY[model_name_clean]
    logger.info(f"Instantiating model class: {model_class.__name__}")
    return model_class(**kwargs)
