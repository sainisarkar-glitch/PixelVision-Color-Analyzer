"""
Chart generation utilities for ColorScope.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from color_mapper import CHART_COLORS


def create_bar_chart(df: pd.DataFrame, title: str, output_path: str | Path) -> None:
    """Create and save a bar chart for color percentages."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    chart_df = df.sort_values("percentage", ascending=False)
    colors = [CHART_COLORS[color] for color in chart_df["color_category"]]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(chart_df["color_category"], chart_df["percentage"], color=colors, edgecolor="black")

    for bar in bars:
        height = bar.get_height()
        if height > 0:
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.1f}%",
                ha="center",
                va="bottom",
                fontsize=9,
            )

    plt.title(title, fontsize=16, fontweight="bold")
    plt.xlabel("Color Category")
    plt.ylabel("Percentage of Image")
    plt.xticks(rotation=35, ha="right")
    plt.ylim(0, max(chart_df["percentage"].max() + 8, 10))
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
