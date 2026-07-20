import time
import requests
from datetime import datetime
from typing import Dict, Any
from tools.verification.base_verifier import BaseVerifier
from tools.verification.verification_utils import is_valid_url_syntax

class HttpVerifier(BaseVerifier):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "BenchmarkVerifier/1.0"})
        
    def verify(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        url = candidate.get("url", "")
        start_time = time.time()
        
        result = {
            "verification_timestamp": datetime.utcnow().isoformat() + "Z",
            "verification_method": "http_head_fallback_get",
            "verification_attempts": 1,
            "http_status": None,
            "content_type": None,
            "content_length": None,
            "redirect_count": 0,
            "final_url": url,
            "verification_notes": [],
            "response_time_ms": 0,
            "verification_status": "FAILED"
        }
        
        if not is_valid_url_syntax(url):
            result["verification_notes"].append("Malformed URL")
            return result
            
        try:
            # Prefer HEAD
            resp = self.session.head(url, allow_redirects=True, timeout=5)
            # Fallback to GET if HEAD fails or doesn't return content length for images
            if resp.status_code >= 400 or (resp.status_code == 200 and not resp.headers.get('Content-Length')):
                resp = self.session.get(url, stream=True, allow_redirects=True, timeout=5)
                # Close the stream immediately to save bandwidth
                resp.close()
                
            result["response_time_ms"] = int((time.time() - start_time) * 1000)
            result["http_status"] = resp.status_code
            result["final_url"] = resp.url
            result["redirect_count"] = len(resp.history)
            
            if resp.status_code != 200:
                result["verification_notes"].append(f"HTTP {resp.status_code}")
                return result
                
            ct = resp.headers.get("Content-Type", "").lower()
            result["content_type"] = ct
            if not ct.startswith("image/"):
                result["verification_notes"].append(f"Invalid MIME type: {ct}")
                return result
                
            cl = resp.headers.get("Content-Length")
            if cl is not None:
                try:
                    size = int(cl)
                    result["content_length"] = size
                    if size == 0:
                        result["verification_notes"].append("Zero-byte response")
                        return result
                except ValueError:
                    pass
            else:
                result["verification_notes"].append("Missing Content-Length")
                
            # Verify source consistency
            dataset_name = candidate.get("dataset_name", "")
            if dataset_name.lower() not in ["paddleocr-public", "cord-v2 (receipts)", "xfund", "funsd", "mlt-2019", "test"]:
                pass # Accept all for now
                
            if "Missing Content-Length" in result["verification_notes"]:
                result["verification_status"] = "PARTIALLY_VERIFIED"
            else:
                result["verification_status"] = "VERIFIED"
                
        except requests.exceptions.TooManyRedirects:
            result["verification_notes"].append("Redirect loop")
        except requests.exceptions.Timeout:
            result["verification_notes"].append("Timeout")
        except requests.exceptions.RequestException as e:
            result["verification_notes"].append(str(e))
            
        return result
