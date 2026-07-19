"""Registry system for metrics and tasks."""
from typing import Dict, Any, Callable

class Registry:
    def __init__(self):
        self._registry: Dict[str, Any] = {}

    def register(self, name: str):
        def decorator(cls_or_func):
            self._registry[name] = cls_or_func
            return cls_or_func
        return decorator

    def get(self, name: str):
        if name not in self._registry:
            raise KeyError(f"'{name}' not found in registry.")
        return self._registry[name]
        
    def list_all(self):
        return list(self._registry.keys())

# Global Registries
TASK_REGISTRY = Registry()
METRIC_REGISTRY = Registry()
EVALUATOR_REGISTRY = Registry()
