from typing import Dict, Any
from .base_report import BaseReport
from .json_writer import write_json_report

class SummaryReport(BaseReport):
    def __init__(self, run_id: str, version: str, source: str):
        self.data = {
            "run_id": run_id,
            "version": version,
            "dataset_source": source,
            "metrics": {}
        }

    def update_metrics(self, key: str, val: Any):
        self.data["metrics"][key] = val

    def generate(self) -> Dict[str, Any]:
        return self.data
