
import platform
import sys

def detect_environment():
    has_tesseract = False
    has_easyocr = False
    has_paddleocr = False
    
    try: import pytesseract; has_tesseract = True
    except: pass
    
    try: import easyocr; has_easyocr = True
    except: pass
    
    try: import paddleocr; has_paddleocr = True
    except: pass
    
    return {
        "os": platform.system(),
        "python_version": sys.version,
        "tesseract_available": has_tesseract,
        "easyocr_available": has_easyocr,
        "paddleocr_available": has_paddleocr
    }
