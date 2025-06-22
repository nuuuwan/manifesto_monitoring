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

    def draw(self):
        plt.close()
        dates = [
            datetime.strptime(item["date"], "%Y-%m-%d")
            for item in self.d_list
        ]

        progress = [item["progress"] for item in self.d_list]

        x_min = min(dates)
        x_max = x_min + relativedelta(years=5)

        plt.figure(figsize=(10, 5))
        plt.plot([x_min, x_max], [0, 1.0], "r--", color="grey")
        plt.plot(dates, progress, color="red", linewidth=3)

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
