"""Script Metrics"""
from .common import BaseMetric
from ..registry import METRIC_REGISTRY

@METRIC_REGISTRY.register("script_accuracy")
class ScriptMetric(BaseMetric):
    def compute(self, prediction, ground_truth) -> float:
        # TODO: Implement script specific metric calculations
        return 0.0
