import os
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.dates import relativedelta
from matplotlib.ticker import PercentFormatter

from mm.monitoring.CompareManifesto import CompareManifesto


class ProgressChart:
    CHART_PATH = os.path.join("images", "progress_chart.png")

    def __init__(self):
        self.d_list = CompareManifesto().get_overall_progress_by_date()

        self.d_list.sort(key=lambda x: x["date"])

    @staticmethod
    def draw_annotate_latest_progress(dates, progress, x_max, x_min):
        latest_date = dates[-1]
        latest_progress = progress[-1]

        total_duration = (x_max - x_min).total_seconds()
        elapsed = (latest_date - x_min).total_seconds()
        expected_progress = (
            elapsed / total_duration
        )  # Value between 0.0 and 1.0

        plt.annotate(
            f"Goal: {expected_progress:.1%}",
            xy=(latest_date, expected_progress),
            xytext=(0, 25),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="grey", lw=1),
            arrowprops=dict(arrowstyle="->", color="grey", lw=1),
        )
        plt.annotate(
            f"{latest_progress:.1%}",
            xy=(latest_date, latest_progress),
            xytext=(25, -25),
            textcoords="offset points",
            ha="left",
            va="top",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="grey", lw=1),
            arrowprops=dict(arrowstyle="->", color="grey", lw=1),
        )

    def draw(self):
        plt.close()
        dates = [
            datetime.strptime(item["date"], "%Y-%m-%d") for item in self.d_list
        ]

        progress = [item["progress"] for item in self.d_list]

        x_min = min(dates)
        x_max = x_min + relativedelta(years=5)

        plt.figure(figsize=(10, 5))
        plt.plot([x_min, x_max], [0, 1.0], linestyle=":", color="grey")
        plt.plot(dates, progress, color="red", linewidth=3)

        self.draw_annotate_latest_progress(dates, progress, x_max, x_min)

        plt.xlabel("Date")
        plt.ylabel("Overall Progress (%)")
        plt.title("Manifesto Items with Cabinet Decisions Match")
        plt.ylim(0, 1.0)
        plt.xlim(min(dates), x_max)
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1.0))
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(self.CHART_PATH, dpi=300)
        plt.close()
