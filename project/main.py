"""
Main orchestration script for the Vision Language Model (VLM) Benchmarking Pipeline.
Loads config, inspects and prepares dataset, runs model inference, evaluates outputs,
generates graphs, and compiles the final PDF report.
"""

import argparse
import logging
import sys
from typing import Optional

from project.benchmark import BenchmarkEngine
from project.config import get_config
from project.evaluation import EvaluationEngine
from project.loader import DatasetLoader
from project.plots import generate_all_plots
from project.report import ReportGenerator
from project.utils import get_system_info, setup_logging

logger = logging.getLogger("vlm_benchmark")


def run_pipeline(
    config_path: Optional[str] = None, max_images_override: Optional[int] = None
) -> int:
    """
    Executes the entire VLM benchmarking workflow end-to-end.

    Args:
        config_path: Path to configuration file.
        max_images_override: Numerical override for the maximum images to evaluate.

    Returns:
        0 on success, 1 on critical error.
    """
    try:
        # 1. Initialize Configuration (Step 1/8)
        config = get_config(config_path)

        # Resolve logging path
        logs_dir = config.get_path("paths.logs_root", "logs")
        setup_logging(logs_dir)

        logger.info("Starting VLM Benchmarking Pipeline Orchestration...")
        print("\n==================================================")
        print("VLM BENCHMARKING PIPELINE — SYSTEM START")
        print("==================================================")

        # 2. Gather System Information & Diagnostics (Step 10/21)
        reports_dir = config.get_path("paths.evaluation_root", "Evaluation") / "Reports"
        sys_info_path = reports_dir / "system_info.json"
        sys_info = get_system_info(sys_info_path)
        print(
            f"Host OS: {sys_info.get('os')} | Detected GPU: {sys_info.get('device_name')}"
        )

        # 3. Load & Validate Dataset (Step 2/3)
        jsonl_path = config.get("dataset.jsonl_path", "signs.jsonl")
        images_dir = config.get_path("dataset.images_dir", "Dataset/images")
        download_enabled = config.get("dataset.download_missing", True)

        print("\nStep 1: Ingesting dataset and validating schema...")
        loader = DatasetLoader(
            jsonl_path=jsonl_path,
            images_dir=str(images_dir),
            download_missing=download_enabled,
        )

        # Determine number of records to process
        max_images = max_images_override
        if max_images is None:
            max_images = config.get("dataset.max_images")

        # 4. Handle missing images (Step 2/8)
        if download_enabled:
            print("\nStep 2: Downloading missing images to local cache...")
            loader.download_and_cache_images(limit=max_images)

        print("\nStep 3: Running dataset health check...")
        validation_report = loader.validate_dataset()
        print("Dataset Health Check Summary:")
        print(
            f"  Total Records in JSONL      : {validation_report.get('total_records')}"
        )
        print(
            f"  Valid Local Cached Images   : {validation_report.get('valid_local_images_count')}"
        )
        print(
            f"  Missing Local Images        : {validation_report.get('missing_images_count')}"
        )
        print(
            f"  Corrupted Images Detected   : {validation_report.get('corrupted_images_count')}"
        )

        # 5. Core Benchmarking Loop (Step 7/8/10)
        print("\nStep 4: Executing Vision Language Model evaluations...")
        benchmark = BenchmarkEngine(config, loader)
        completed_models = benchmark.run_all(max_images=max_images)

        if not completed_models:
            logger.warning(
                "No models completed inference successfully. Skipping evaluation/reporting."
            )
            print("\nError: No benchmarking runs finished. Pipeline aborted.")
            return 1

        # 6. Evaluation & Scoring (Step 11/14)
        print("\nStep 5: Scoring model predictions against ground truth...")
        eval_engine = EvaluationEngine(config, loader)
        all_eval_results = []

        for model in completed_models:
            logger.info(f"Evaluating results for {model}...")
            model_results = eval_engine.evaluate_model(model)
            all_eval_results.extend(model_results)

        if not all_eval_results:
            logger.error("No predictions evaluated. Cannot generate leaderboard.")
            print("Error: No prediction files could be parsed. Report aborted.")
            return 1

        # Generate leaderboard Excel/CSV
        leaderboard_df = eval_engine.generate_leaderboard(all_eval_results)
        print("\nLeaderboard Standings:")
        print(
            leaderboard_df[
                [
                    "Rank",
                    "model",
                    "Total Images",
                    "Parse Success Rate (%)",
                    "Avg Generation Time (s)",
                ]
            ].to_string(index=False)
        )

        # 7. Visualization Graph Generation (Step 13)
        print("\nStep 6: Drawing evaluation data visualizations...")
        graphs_dir = config.get_path("paths.evaluation_root", "Evaluation") / "Graphs"
        leaderboard_csv = reports_dir / "leaderboard.csv"
        reports_dir / "image_level_scores.xlsx"

        generate_all_plots(leaderboard_path=leaderboard_csv, output_dir=graphs_dir)

        # 8. Compile PDF Report (Step 15)
        print("\nStep 7: Compiling final PDF report document...")
        report_gen = ReportGenerator(config)
        report_gen.compile_pdf()

        print("\n==================================================")
        print("VLM BENCHMARKING PIPELINE — PIPELINE RUN COMPLETE")
        print("==================================================")
        return 0

    except Exception as e:
        logger.critical(
            f"Pipeline crashed due to unhandled exception: {e}", exc_info=True
        )
        print(f"\nCRITICAL PIPELINE ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="VLM Benchmarking Pipeline Orchestrator"
    )
    parser.add_argument(
        "--config", type=str, default=None, help="Path to the config.yaml settings file"
    )
    parser.add_argument(
        "--max-images",
        type=int,
        default=None,
        help="Override maximum number of images to process",
    )

    args = parser.parse_args()
    sys.exit(run_pipeline(config_path=args.config, max_images_override=args.max_images))
