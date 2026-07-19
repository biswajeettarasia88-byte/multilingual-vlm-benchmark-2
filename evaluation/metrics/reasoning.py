"""Reasoning Metrics"""
from .common import BaseMetric
from ..registry import METRIC_REGISTRY

@METRIC_REGISTRY.register("reasoning_accuracy")
class ReasoningMetric(BaseMetric):
    def compute(self, prediction, ground_truth) -> float:
        # TODO: Implement reasoning specific metric calculations
        return 0.0
