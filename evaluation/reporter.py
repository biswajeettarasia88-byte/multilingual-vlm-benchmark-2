"""Report Generator."""

class ReportGenerator:
    def generate_score(self, metrics: dict) -> dict:
        """Generate score.json format."""
        return {"scores": metrics}

    def generate_report(self, scores: dict, validations: list) -> dict:
        """Generate report.json combining scores and validation errors."""
        return {
            "overall_score": 0.0,
            "per_task_score": scores,
            "warnings": validations
        }
