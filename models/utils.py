"""
Shared utilities for Model Adapters.
"""
import base64
import time
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

def encode_image_base64(image_path: str) -> str:
    """Encode image to base64 string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def retry_with_backoff(func: Callable, retries: int = 3, backoff_in_seconds: int = 1, **kwargs) -> Any:
    """Execute a function with exponential backoff retry logic."""
    for i in range(retries):
        try:
            return func(**kwargs)
        except Exception as e:
            if i == retries - 1:
                logger.error(f"Function failed after {retries} retries: {e}")
                raise
            sleep_time = backoff_in_seconds * (2 ** i)
            logger.warning(f"Error occurred: {e}. Retrying in {sleep_time}s...")
            time.sleep(sleep_time)
