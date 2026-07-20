from urllib.parse import urlparse

def is_valid_url_syntax(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return bool(parsed.scheme and parsed.netloc)
    except:
        return False
