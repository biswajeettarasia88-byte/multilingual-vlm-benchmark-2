import logging
import json
from datetime import datetime
import sys

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "module": record.module,
            "event": getattr(record, "event", "execution"),
            "candidate_id": getattr(record, "candidate_id", "N/A"),
            "dataset_source": getattr(record, "dataset_source", "N/A"),
            "message": record.getMessage()
        }
        return json.dumps(log_obj)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
