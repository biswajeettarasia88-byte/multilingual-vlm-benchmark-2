from typing import List, Dict, Optional
from .base import BaseDownloader
from .registry import register_downloader

@register_downloader("wikimedia")
class WikimediaDownloader(BaseDownloader):
    def discover_metadata(self, query: str) -> List[Dict]:
        return []

    def validate_metadata(self, metadata: Dict) -> bool:
        return True

    def download(self, url: str, dest: str) -> bool:
        return False

    def verify(self, filepath: str, expected_hash: Optional[str] = None) -> bool:
        return False
