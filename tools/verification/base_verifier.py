from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseVerifier(ABC):
    @abstractmethod
    def verify(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        pass
