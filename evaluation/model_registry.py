
MODELS = {
    "tesseract": {
        "model_id": "tesseract-ocr",
        "model_name": "Tesseract",
        "requires_binary": True
    },
    "easyocr": {
        "model_id": "easyocr-v1",
        "model_name": "EasyOCR",
        "requires_gpu": True
    },
    "paddleocr": {
        "model_id": "paddleocr-v2",
        "model_name": "PaddleOCR",
        "requires_gpu": False
    }
}
