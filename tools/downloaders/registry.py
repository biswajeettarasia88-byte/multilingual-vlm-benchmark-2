from typing import Dict, Type
from .base import BaseDownloader

_DOWNLOADERS: Dict[str, Type[BaseDownloader]] = {}

def register_downloader(source_name: str):
    def wrapper(cls: Type[BaseDownloader]):
        _DOWNLOADERS[source_name.lower()] = cls
        return cls
    return wrapper

def get_downloader(source_name: str) -> BaseDownloader:
    cls = _DOWNLOADERS.get(source_name.lower())
    if not cls:
        raise ValueError(f"No downloader registered for source: {source_name}")
    return cls()
