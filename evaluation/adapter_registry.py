
from .environment_detector import detect_environment

env = detect_environment()

class TesseractAdapter:
    def __init__(self):
        self.name = "Tesseract"
        self.version = "1.0"
        
    def check_availability(self):
        if not env["tesseract_available"]:
            return "IMPORT_FAILED"
        return "AVAILABLE"

    def infer(self, path): pass

class EasyOCRAdapter:
    def __init__(self):
        self.name = "EasyOCR"
        self.version = "1.0"
        
    def check_availability(self):
        if not env["easyocr_available"]:
            return "NOT_INSTALLED"
        return "AVAILABLE"

    def infer(self, path): pass

class PaddleOCRAdapter:
    def __init__(self):
        self.name = "PaddleOCR"
        self.version = "1.0"
        
    def check_availability(self):
        if not env["paddleocr_available"]:
            return "NOT_INSTALLED"
        return "AVAILABLE"

    def infer(self, path): pass

ADAPTERS = {
    "tesseract": TesseractAdapter,
    "easyocr": EasyOCRAdapter,
    "paddleocr": PaddleOCRAdapter
}
