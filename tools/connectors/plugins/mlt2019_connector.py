
from tools.connectors.base_connector import BaseConnector

class MLT2019Connector(BaseConnector):
    def connect(self): return True
    def validate_dataset(self): return True
    def get_dataset_information(self):
        return {
            "dataset_name": "MLT2019",
            "official_homepage": "https://rrc.cvc.uab.es/?ch=15",
            "official_repository": "N/A",
            "official_download_page": "https://rrc.cvc.uab.es/?ch=15",
            "citation": "Nayef et al. ICDAR2019 Robust Reading Challenge on Multi-lingual Scene Text Detection",
            "archive_format": "zip",
            "languages": ["ar", "bn", "zh", "hi", "ja", "ko", "pt", "en"],
            "categories": ["scene_text"]
        }
    def get_license_information(self): return "Custom (Research Only)"
    def get_distribution_method(self): return "ZIP_ARCHIVE"
    def get_dataset_version(self): return "2019"
    def get_supported_splits(self): return ["train", "test"]
    def get_documentation(self): return "RRC Website"
    def enumeration_capability(self):
        return "ENUMERATION_REQUIRES_AUTHENTICATION", "Requires account creation on RRC portal."
    def resolve_download_method(self): return "AUTHENTICATION_REQUIRED"
