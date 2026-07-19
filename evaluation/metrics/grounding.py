"""Grounding Metrics"""
from .common import BaseMetric
from ..registry import METRIC_REGISTRY

@METRIC_REGISTRY.register("grounding_accuracy")
class GroundingMetric(BaseMetric):
    def compute(self, prediction, ground_truth) -> float:
        # TODO: Implement grounding specific metric calculations
        return 0.0
