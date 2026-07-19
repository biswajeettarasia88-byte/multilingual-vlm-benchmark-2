from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class BaseDownloader(ABC):
    @abstractmethod
    def discover_metadata(self, query: str) -> List[Dict]:
        pass

    @abstractmethod
    def validate_metadata(self, metadata: Dict) -> bool:
        pass

    @abstractmethod
    def download(self, url: str, dest: str) -> bool:
        pass

    @abstractmethod
    def verify(self, filepath: str, expected_hash: Optional[str] = None) -> bool:
        pass
