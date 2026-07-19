"""Evaluation Pipeline Orchestrator."""
from .validator import SchemaValidator
from .reporter import ReportGenerator

class EvaluationPipeline:
    def __init__(self):
        self.validator = SchemaValidator()
        self.reporter = ReportGenerator()
        
    def run(self, prediction_path, expected_path):
        """
        Flow:
        1. Prediction Load
        2. Schema Validation
        3. Task Detection
        4. Metric Selection
        5. Metric Execution
        6. Score Aggregation
        7. Report Generation
        8. Leaderboard Export
        """
        pass
