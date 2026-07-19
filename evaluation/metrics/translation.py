"""Translation Metrics"""
from .common import BaseMetric
from ..registry import METRIC_REGISTRY

@METRIC_REGISTRY.register("translation_accuracy")
class TranslationMetric(BaseMetric):
    def compute(self, prediction, ground_truth) -> float:
        # TODO: Implement translation specific metric calculations
        return 0.0
