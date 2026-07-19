
import requests
from tools.downloaders.base import BaseDownloader

class HTTPRawDownloader(BaseDownloader):
    """Source-agnostic downloader for raw HTTP file endpoints commonly used by open research datasets (AWS S3, GCS, HF Resolve)."""
    
    def discover_metadata(self, source_uri: str, **kwargs) -> list:
        # For this integration, we expect the pipeline to pass explicit metadata for evaluation.
        return []

    def validate_metadata(self, metadata: dict) -> bool:
        return "url" in metadata and metadata["url"].startswith("http")

    def download(self, metadata: dict, output_path: str) -> bool:
        try:
            res = requests.get(metadata["url"], headers={"User-Agent": "ResearchPipeline/1.0"}, stream=True, timeout=15)
            res.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in res.iter_content(8192):
                    f.write(chunk)
            return True
        except Exception as e:
            print(f"Download failed for {metadata.get('url')}: {e}")
            return False

    def verify(self, output_path: str, expected_checksum: str = None) -> bool:
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            return False
        return True
