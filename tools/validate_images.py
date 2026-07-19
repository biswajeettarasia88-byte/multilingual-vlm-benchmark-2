"""
Tool: validate_images.py
Description: Validates image integrity, resolution, format, and color space.
"""
import os
import json
try:
    from PIL import Image, ImageStat
except ImportError:
    pass

class ImageValidator:
    def __init__(self, min_res: int = 1024, min_short_side: int = 768):
        self.min_res = min_res
        self.min_short_side = min_short_side
        
    def validate(self, filepath: str) -> dict:
        result = {"valid": False, "errors": [], "metadata": {}}
        try:
            with Image.open(filepath) as img:
                img.verify()
        except Exception as e:
            result["errors"].append(f"Corrupt image: {str(e)}")
            return result
            
        try:
            with Image.open(filepath) as img:
                result["metadata"]["format"] = img.format
                result["metadata"]["mode"] = img.mode
                result["metadata"]["size"] = img.size
                
                if img.format not in ['JPEG', 'PNG']:
                    result["errors"].append(f"Unsupported format: {img.format}")
                if img.mode != 'RGB':
                    result["errors"].append(f"Invalid color space: {img.mode}. Expected RGB.")
                    
                w, h = img.size
                if max(w, h) < self.min_res:
                    result["errors"].append(f"Resolution {w}x{h} below minimum {self.min_res}")
                if min(w, h) < self.min_short_side:
                    result["errors"].append(f"Short side {min(w,h)} below minimum {self.min_short_side}")
                    
                # Store exif if available
                exif = img.getexif()
                result["metadata"]["has_exif"] = bool(exif)
                
        except Exception as e:
            result["errors"].append(f"Processing error: {str(e)}")
            
        if not result["errors"]:
            result["valid"] = True
            
        return result

def run_validation(directory: str, output_path: str):
    validator = ImageValidator()
    report = {"valid": [], "invalid": []}
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                path = os.path.join(root, file)
                res = validator.validate(path)
                if res["valid"]:
                    report["valid"].append(path)
                else:
                    report["invalid"].append({"path": path, "errors": res["errors"]})
                    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    pass
