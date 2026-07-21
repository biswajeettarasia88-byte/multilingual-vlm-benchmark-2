
from abc import ABC, abstractmethod

class BaseIngestion(ABC):
    @abstractmethod
    def ingest(self, filepath): pass
