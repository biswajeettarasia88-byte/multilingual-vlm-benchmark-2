
from tools.connectors.base_connector import BaseConnector

class FUNSDConnector(BaseConnector):
    def connect(self): return True
    def validate_dataset(self): return True
    def get_dataset_information(self):
        return {
            "dataset_name": "FUNSD",
            "official_homepage": "https://guillaumejaume.github.io/FUNSD/",
            "official_repository": "https://guillaumejaume.github.io/FUNSD/",
            "official_download_page": "https://guillaumejaume.github.io/FUNSD/download/",
            "citation": "Jaume et al. FUNSD: A Dataset for Form Understanding in Noisy Scanned Documents",
            "archive_format": "zip",
            "languages": ["en"],
            "categories": ["form"]
        }
    def get_license_information(self): return "CC-BY-4.0"
    def get_distribution_method(self): return "ZIP_ARCHIVE"
    def get_dataset_version(self): return "1.0"
    def get_supported_splits(self): return ["train", "test"]
    def get_documentation(self): return "Official Website"
    def enumeration_capability(self):
        return "ENUMERATION_REQUIRES_DOWNLOAD", "Dataset is distributed as a single ZIP file containing all images and annotations."
    def resolve_download_method(self): return "DOWNLOADABLE"
