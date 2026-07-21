
from tools.connectors.base_connector import BaseConnector

class PaddleOCRConnector(BaseConnector):
    def connect(self): return True
    def validate_dataset(self): return True
    def get_dataset_information(self):
        return {
            "dataset_name": "PaddleOCR",
            "official_homepage": "https://github.com/PaddlePaddle/PaddleOCR",
            "official_repository": "https://github.com/PaddlePaddle/PaddleOCR",
            "official_download_page": "https://github.com/PaddlePaddle/PaddleOCR",
            "citation": "PaddleOCR Team",
            "archive_format": "tar",
            "languages": ["zh", "en"],
            "categories": ["scene_text", "document"]
        }
    def get_license_information(self): return "Apache-2.0"
    def get_distribution_method(self): return "TAR_ARCHIVE"
    def get_dataset_version(self): return "2.0"
    def get_supported_splits(self): return ["train", "val"]
    def get_documentation(self): return "GitHub README"
    def enumeration_capability(self):
        return "ENUMERATION_REQUIRES_DOWNLOAD", "Assets bundled in tarball."
    def resolve_download_method(self): return "DOWNLOADABLE"
