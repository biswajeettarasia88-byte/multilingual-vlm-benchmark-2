from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseReport(ABC):
    @abstractmethod
    def generate(self) -> Dict[str, Any]:
        pass
