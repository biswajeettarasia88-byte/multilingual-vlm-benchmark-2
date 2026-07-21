
from abc import ABC, abstractmethod

class BaseConnector(ABC):
    @abstractmethod
    def connect(self): pass
    
    @abstractmethod
    def validate_dataset(self): pass
    
    @abstractmethod
    def get_dataset_information(self): pass
    
    @abstractmethod
    def get_license_information(self): pass
    
    @abstractmethod
    def get_distribution_method(self): pass
    
    @abstractmethod
    def get_dataset_version(self): pass
    
    @abstractmethod
    def get_supported_splits(self): pass
    
    @abstractmethod
    def get_documentation(self): pass
    
    @abstractmethod
    def enumeration_capability(self): pass
    
    @abstractmethod
    def resolve_download_method(self): pass
