"""Core evaluator interface."""
from .registry import EVALUATOR_REGISTRY

@EVALUATOR_REGISTRY.register("base_evaluator")
class BaseEvaluator:
    def evaluate(self, prediction: dict, expected: dict) -> dict:
        """Execute metrics based on tasks."""
        return {}
