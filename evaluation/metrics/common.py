"""Common metric interfaces."""
from abc import ABC, abstractmethod
from typing import Any

class BaseMetric(ABC):
    @abstractmethod
    def compute(self, prediction: Any, ground_truth: Any) -> float:
        """Compute the metric score."""
        pass
