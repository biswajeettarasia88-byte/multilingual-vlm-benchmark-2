"""
Configuration loader and folder setup module for VLM benchmarking.
Loads settings from config.yaml, sets random seeds, and creates the folder structure.
"""

import logging
import os
import random
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

logger = logging.getLogger("vlm_benchmark")

# Helper to find the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class BenchmarkConfig:
    """BenchmarkConfig handles loading and parsing YAML configurations and directory setup."""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # Look for config.yaml in the project directory first
            config_path = str(PROJECT_ROOT / "project" / "configs" / "config.yaml")
            if not os.path.exists(config_path):
                # Fallback to local workspace root config.yaml
                config_path = str(PROJECT_ROOT / "config.yaml")
                if not os.path.exists(config_path):
                    # Fallback to whatever is in the current working directory
                    config_path = "config.yaml"

        self.config_path = Path(config_path).resolve()
        self.data: Dict[str, Any] = {}
        self.load_config()
        self.setup_directories()
        self.set_reproducibility_seeds()

    def load_config(self) -> None:
        """Loads and parses the config.yaml file."""
        if not self.config_path.exists():
            # If config file doesn't exist, create a default dictionary to avoid crash
            logger.warning(
                f"Configuration file not found at {self.config_path}. Using fallback defaults."
            )
            self.data = self._get_fallback_defaults()
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.data = yaml.safe_load(f) or {}
            logger.info(f"Successfully loaded configuration from {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load configuration from {self.config_path}: {e}")
            self.data = self._get_fallback_defaults()

    def _get_fallback_defaults(self) -> Dict[str, Any]:
        """Provides default configurations if yaml fails to load."""
        return {
            "dataset": {
                "jsonl_path": "signs.jsonl",
                "images_dir": "Dataset/images",
                "max_images": 10,
                "download_missing": True,
                "sample_subset": True,
            },
            "paths": {
                "dataset_root": "Dataset",
                "output_root": "Outputs",
                "evaluation_root": "Evaluation",
                "logs_root": "logs",
                "prompts_root": "prompts",
                "report_pdf": "Evaluation/Reports/Final_Report.pdf",
                "leaderboard_csv": "Evaluation/Reports/leaderboard.csv",
                "leaderboard_xlsx": "Evaluation/Reports/leaderboard.xlsx",
            },
            "runtime": {
                "device": "cuda",
                "random_seed": 42,
                "deterministic": True,
                "resume": True,
                "default_precision": "bf16",
                "quantization": "4bit",
            },
            "models": {
                "gpt4o": {
                    "enabled": True,
                    "model_name": "gpt-4o",
                    "api_key_env": "OPENAI_API_KEY",
                    "temperature": 0.0,
                },
                "gemini": {
                    "enabled": True,
                    "model_name": "gemini-2.5-flash",
                    "api_key_env": "GEMINI_API_KEY",
                    "temperature": 0.0,
                },
            },
            "prompt": {"prompt_file": "prompts/benchmark_prompt.txt"},
            "evaluation": {
                "cultural_eval": {
                    "method": "dictionary",
                    "dictionary_keywords": ["india", "indian"],
                },
                "weights": {
                    "format_compliance": 0.1,
                    "ocr_accuracy": 0.25,
                    "caption_quality": 0.15,
                    "scene_understanding": 0.15,
                    "object_detection": 0.15,
                    "cultural_accuracy": 0.1,
                    "speed_score": 0.1,
                },
            },
        }

    def setup_directories(self) -> None:
        """Automatically creates the project folder structure as specified in Step 8."""
        # Main root paths
        dataset_root = self.get_path("paths.dataset_root", "Dataset")
        output_root = self.get_path("paths.output_root", "Outputs")
        evaluation_root = self.get_path("paths.evaluation_root", "Evaluation")
        logs_root = self.get_path("paths.logs_root", "logs")
        prompts_root = self.get_path("paths.prompts_root", "prompts")

        # Create base folders
        for folder in [
            dataset_root,
            output_root,
            evaluation_root,
            logs_root,
            prompts_root,
        ]:
            Path(folder).mkdir(parents=True, exist_ok=True)

        # Output subfolders for each VLM
        vlm_subfolders = [
            "GPT4o",
            "Gemini",
            "InternVL",
            "MiniCPM",
            "Qwen",
            "Molmo",
            "Phi4",
            "Llama",
        ]
        for sub in vlm_subfolders:
            Path(output_root / sub).mkdir(parents=True, exist_ok=True)

        # Evaluation subfolders
        eval_subfolders = ["Graphs", "Reports", "Logs"]
        for sub in eval_subfolders:
            Path(evaluation_root / sub).mkdir(parents=True, exist_ok=True)

        logger.info("Project directory structure verified / created successfully.")

    def set_reproducibility_seeds(self) -> None:
        """Sets random seeds for numpy, random, and torch to ensure reproducible runs."""
        seed = self.get("runtime.random_seed", 42)
        random.seed(seed)

        try:
            import numpy as np

            np.random.seed(seed)
        except ImportError:
            pass

        try:
            import torch

            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)

            deterministic = self.get("runtime.deterministic", True)
            if deterministic:
                torch.backends.cudnn.deterministic = True
                torch.backends.cudnn.benchmark = False
        except ImportError:
            pass

        logger.info(
            f"Random seed set to {seed} (Deterministic: {self.get('runtime.deterministic', True)})"
        )

    def get(self, key_path: str, default: Any = None) -> Any:
        """Retrieves a nested configuration value using dot notation (e.g., 'dataset.images_dir')."""
        keys = key_path.split(".")
        val = self.data
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val

    def get_path(self, key_path: str, default: str) -> Path:
        """Retrieves a config path and returns it as a resolved absolute Path object."""
        path_str = self.get(key_path, default)
        return PROJECT_ROOT / path_str


# Global configuration instance (lazy initialized)
_config_instance: Optional[BenchmarkConfig] = None


def get_config(config_path: Optional[str] = None) -> BenchmarkConfig:
    """Global getter for the configuration instance."""
    global _config_instance
    if _config_instance is None or config_path is not None:
        _config_instance = BenchmarkConfig(config_path)
    return _config_instance
