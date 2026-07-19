"""Language Metrics"""
from .common import BaseMetric
from ..registry import METRIC_REGISTRY

@METRIC_REGISTRY.register("language_accuracy")
class LanguageMetric(BaseMetric):
    def compute(self, prediction, ground_truth) -> float:
        # TODO: Implement language specific metric calculations
        return 0.0
