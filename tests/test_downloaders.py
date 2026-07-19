import pytest
from tools.downloaders.registry import get_downloader
from tools.downloaders.base import BaseDownloader

# Import subclasses to trigger decorators
import tools.downloaders.wikimedia
import tools.downloaders.huggingface
import tools.downloaders.kaggle
import tools.downloaders.zenodo

def test_registry():
    dl = get_downloader("wikimedia")
    assert isinstance(dl, BaseDownloader)
    
    dl_hf = get_downloader("huggingface")
    assert isinstance(dl_hf, BaseDownloader)
    
    with pytest.raises(ValueError):
        get_downloader("nonexistent_source")
        
def test_base_methods():
    dl = get_downloader("kaggle")
    assert dl.discover_metadata("test") == []
    assert dl.validate_metadata({}) == True
    assert dl.download("url", "dest") == False
    assert dl.verify("path") == False
