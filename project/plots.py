import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger("vlm_benchmark")

COLORS = [
    "#4361EE",
    "#4CC9F0",
    "#F72585",
    "#7209B7",
    "#3F37C9",
    "#FF9F1C",
    "#2EC4B6",
    "#E71D36",
]


def apply_plot_style():
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.size"] = 10
    plt.rcParams["axes.grid"] = True


def plot_ranking(df: pd.DataFrame, output_path: Path):
    apply_plot_style()
    plt.figure(figsize=(8, 4.5))
    df_sorted = df.sort_values(by="Parse Success Rate (%)", ascending=True)
    bars = plt.barh(
        df_sorted["model"],
        df_sorted["Parse Success Rate (%)"],
        color=COLORS[: len(df_sorted)],
    )
    plt.title("VLM Parse Success Rate (%)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def generate_all_plots(leaderboard_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        df = pd.read_csv(leaderboard_path)
        plot_ranking(df, output_dir / "ranking.png")
        logger.info("Graphs generated successfully.")
    except Exception as e:
        logger.error(f"Graph generation failed: {e}")
