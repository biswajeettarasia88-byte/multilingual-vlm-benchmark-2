
from tools.connectors.base_connector import BaseConnector

class CORDConnector(BaseConnector):
    def connect(self): return True
    def validate_dataset(self): return True
    def get_dataset_information(self):
        return {
            "dataset_name": "CORD",
            "official_homepage": "https://github.com/clovaai/cord",
            "official_repository": "https://github.com/clovaai/cord",
            "official_download_page": "https://github.com/clovaai/cord",
            "citation": "Park et al. CORD: A Consolidated Receipt Dataset for Post-OCR Parsing",
            "archive_format": "zip",
            "languages": ["id"],
            "categories": ["receipt"]
        }
    def get_license_information(self): return "CC-BY-4.0"
    def get_distribution_method(self): return "ZIP_ARCHIVE"
    def get_dataset_version(self): return "1.0"
    def get_supported_splits(self): return ["train", "dev", "test"]
    def get_documentation(self): return "GitHub README"
    def enumeration_capability(self):
        return "ENUMERATION_REQUIRES_DOWNLOAD", "Assets are bundled in a zip file."
    def resolve_download_method(self): return "DOWNLOADABLE"
