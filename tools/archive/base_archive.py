
from abc import ABC, abstractmethod

class BaseArchive(ABC):
    @abstractmethod
    def validate(self): pass
    @abstractmethod
    def extract(self, destination): pass
    @abstractmethod
    def enumerate_contents(self): pass
