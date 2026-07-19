"""
Abstract Base Class for Vision Language Model Adapters.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseVisionLanguageModel(ABC):
    """Abstract interface for all VLM benchmark adapters."""
    
    @abstractmethod
    def load(self, **kwargs) -> bool:
        """Initialize the model or API client."""
        pass
        
    @abstractmethod
    def predict(self, image_path: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Run inference on a single image."""
        pass
        
    @abstractmethod
    def batch_predict(self, instances: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
        """Run batch inference."""
        pass
        
    @abstractmethod
    def health_check(self) -> bool:
        """Verify API connectivity or model readiness."""
        pass
        
    @abstractmethod
    def metadata(self) -> Dict[str, str]:
        """Return model metadata (version, parameters, provider)."""
        pass
        
    @abstractmethod
    def close(self):
        """Clean up resources."""
        pass
