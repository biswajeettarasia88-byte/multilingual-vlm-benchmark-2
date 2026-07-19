"""Ocr Metrics"""
from .common import BaseMetric
from ..registry import METRIC_REGISTRY

@METRIC_REGISTRY.register("ocr_accuracy")
class OcrMetric(BaseMetric):
    def compute(self, prediction, ground_truth) -> float:
        # TODO: Implement ocr specific metric calculations
        return 0.0
