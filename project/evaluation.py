"""
Evaluation engine for calculating VLM benchmarking metrics.
Computes generation success rate, parse success rate, and speed metrics.
"""

import json
import logging
from typing import Any, Dict, List

import pandas as pd

from project.config import BenchmarkConfig
from project.loader import DatasetLoader

logger = logging.getLogger("vlm_benchmark")


class EvaluationEngine:
    """EvaluationEngine handles metrics aggregation and leaderboard generation."""

    def __init__(self, config: BenchmarkConfig, loader: DatasetLoader):
        self.config = config
        self.loader = loader
        self.output_root = config.get_path("paths.output_root", "Outputs")
        self.reports_root = (
            config.get_path("paths.evaluation_root", "Evaluation") / "Reports"
        )
        self.reports_root.mkdir(parents=True, exist_ok=True)

    def evaluate_model(self, model_key: str) -> List[Dict[str, Any]]:
        """Evaluates saved output files for a specific model."""
        model_dir = self.output_root / model_key.capitalize()
        if not model_dir.exists():
            logger.warning(
                f"Output directory {model_dir} does not exist. Skipping evaluation."
            )
            return []

        results = []
        records_map = {
            rec.get(self.loader.schema.id_field): rec for rec in self.loader.records
        }

        # Load the CSV log if it exists to get exact status failures
        csv_log_path = self.reports_root.parent / "Logs" / f"{model_key}_benchmark.csv"
        csv_data = {}
        if csv_log_path.exists():
            try:
                df_csv = pd.read_csv(csv_log_path)
                for _, row in df_csv.iterrows():
                    csv_data[row["image_id"]] = row["status"]
            except Exception as e:
                logger.error(f"Failed to read CSV log: {e}")

        for p in model_dir.glob("*.json"):
            if p.name.endswith("_raw.json") or p.name.endswith("_raw.txt"):
                continue

            try:
                with open(p, "r", encoding="utf-8") as f:
                    output_data = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load output file {p}: {e}")
                continue

            image_id = output_data.get("image_id", p.stem)

            # Extract metrics
            processing_time = output_data.get("processing_time_sec", 0.0)
            has_error = "error" in output_data

            # Check fields
            ocr_text = output_data.get("ocr_text", "")
            scripts = output_data.get("scripts", [])
            languages = output_data.get("languages", [])
            multi_ext = output_data.get("multilingual_extraction", {})
            text_qa = output_data.get("text_qa", {})

            ocr_success = 1 if ocr_text else 0
            script_success = 1 if len(scripts) > 0 else 0
            lang_success = 1 if len(languages) > 0 else 0

            trans_complete = (
                1
                if multi_ext
                and all(
                    k in multi_ext and multi_ext[k]
                    for k in ["original", "romanized", "english_translation"]
                )
                else 0
            )
            qa_complete = (
                1
                if text_qa and text_qa.get("question") and text_qa.get("answer")
                else 0
            )

            is_invalid = has_error or (not ocr_text and not scripts and not languages)
            missing_outputs = (
                (1 - ocr_success)
                + (1 - script_success)
                + (1 - lang_success)
                + (1 - trans_complete)
                + (1 - qa_complete)
            )

            # Record result
            results.append(
                {
                    "image_id": image_id,
                    "model": model_key,
                    "generation_success": 0 if has_error else 1,
                    "parse_success": 0 if is_invalid else 1,
                    "ocr_success": ocr_success,
                    "script_success": script_success,
                    "lang_success": lang_success,
                    "trans_complete": trans_complete,
                    "qa_complete": qa_complete,
                    "invalid_outputs": 1 if is_invalid else 0,
                    "missing_outputs": missing_outputs,
                    "processing_time": processing_time,
                    "failure": 1 if has_error else 0,
                }
            )

        # Check against ground truth count to find completely missed files
        evaluated_ids = {r["image_id"] for r in results}
        for image_id in records_map.keys():
            if image_id not in evaluated_ids:
                results.append(
                    {
                        "image_id": image_id,
                        "model": model_key,
                        "generation_success": 0,
                        "parse_success": 0,
                        "ocr_success": 0,
                        "script_success": 0,
                        "lang_success": 0,
                        "trans_complete": 0,
                        "qa_complete": 0,
                        "invalid_outputs": 1,
                        "missing_outputs": 5,
                        "processing_time": 0.0,
                        "failure": 1,
                    }
                )

        return results

    def generate_leaderboard(self, all_results: List[Dict[str, Any]]) -> pd.DataFrame:
        """Aggregates image-level evaluation results, computes statistics, and compiles the leaderboard."""
        if not all_results:
            logger.warning("No evaluation results available to compile leaderboard.")
            return pd.DataFrame()

        df = pd.DataFrame(all_results)

        # Group by Model
        grouped = df.groupby("model").agg(
            {
                "image_id": "count",
                "generation_success": "mean",
                "parse_success": "mean",
                "ocr_success": "mean",
                "script_success": "mean",
                "lang_success": "mean",
                "trans_complete": "mean",
                "qa_complete": "mean",
                "invalid_outputs": "sum",
                "missing_outputs": "sum",
                "processing_time": "mean",
                "failure": "mean",
            }
        )

        # Convert to percentages
        for col in [
            "generation_success",
            "parse_success",
            "ocr_success",
            "script_success",
            "lang_success",
            "trans_complete",
            "qa_complete",
            "failure",
        ]:
            grouped[col] = grouped[col] * 100

        grouped = grouped.reset_index()

        # Rename columns
        rename_map = {
            "image_id": "Total Images",
            "generation_success": "Generation Success Rate (%)",
            "parse_success": "Parse Success Rate (%)",
            "ocr_success": "OCR Success (%)",
            "script_success": "Script Detection (%)",
            "lang_success": "Lang Detection (%)",
            "trans_complete": "Trans Completeness (%)",
            "qa_complete": "QA Completeness (%)",
            "invalid_outputs": "Invalid Outputs",
            "missing_outputs": "Missing Outputs",
            "processing_time": "Avg Generation Time (s)",
            "failure": "Failure Rate (%)",
        }
        grouped = grouped.rename(columns=rename_map)

        # Rank models by Parse Success Rate and then Speed
        grouped = grouped.sort_values(
            by=["Parse Success Rate (%)", "Avg Generation Time (s)"],
            ascending=[False, True],
        )
        grouped["Rank"] = range(1, len(grouped) + 1)

        # Save Leaderboard files
        leaderboard_csv_path = self.reports_root / "leaderboard.csv"
        leaderboard_xlsx_path = self.reports_root / "leaderboard.xlsx"

        try:
            grouped.to_csv(leaderboard_csv_path, index=False)
            grouped.to_excel(leaderboard_xlsx_path, index=False)
            logger.info(f"Leaderboard exported to CSV: {leaderboard_csv_path}")
        except Exception as e:
            logger.error(f"Failed to export leaderboard: {e}")

        return grouped
