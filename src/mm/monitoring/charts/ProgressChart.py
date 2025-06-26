import os
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.dates import relativedelta
from matplotlib.ticker import PercentFormatter

from mm.monitoring.CompareManifesto import CompareManifesto


class ProgressChart:
    CHART_PATH = os.path.join("images", "progress_chart.png")

    def __init__(self):
        d_list = CompareManifesto().get_overall_progress_by_date()
        d_list.sort(key=lambda x: x["date"])
        self.dates = [
            datetime.strptime(item["date"], "%Y-%m-%d") for item in d_list
        ]
        self.progress = [item["progress"] for item in d_list]

        self.x_min = min(self.dates)
        self.x_max = self.x_min + relativedelta(years=5)

        self.latest_date = self.dates[-1]
        self.latest_progress = self.progress[-1]

        total_duration = (self.x_max - self.x_min).total_seconds()
        elapsed = (self.latest_date - self.x_min).total_seconds()
        self.expected_progress = elapsed / total_duration

    def draw_annotate_latest_progress(self):

        plt.annotate(
            f"Expected: {self.expected_progress:.1%}",
            color="grey",
            xy=(self.latest_date, self.expected_progress),
            xytext=(-25, 0),
            textcoords="offset points",
            ha="right",
            va="center",
            fontsize=9,
            arrowprops=dict(arrowstyle="->", color="grey", lw=1),
        )
        plt.annotate(
            f"Actual: {self.latest_progress:.1%}",
            color="red",
            xy=(self.latest_date, self.latest_progress),
            xytext=(25, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=10,
            arrowprops=dict(arrowstyle="->", color="grey", lw=1),
        )

    def draw(self):
        plt.close()

        plt.figure(figsize=(10, 5))
        plt.plot(
            [self.x_min, self.x_max], [0, 1.0], linestyle=":", color="grey"
        )
        plt.plot(self.dates, self.progress, color="red", linewidth=3)

        self.draw_annotate_latest_progress()

        plt.xlabel("Date")
        plt.ylabel("Overall Progress (%)")
        date_str = self.latest_date.strftime("%Y-%m-%d")
        plt.title(f"Manifesto Items vs. Cabinet Decisions (As of {date_str})")
        plt.ylim(0, 1.0)
        plt.xlim(self.x_min, self.x_max)
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1.0))
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(self.CHART_PATH, dpi=300)
        plt.close()
