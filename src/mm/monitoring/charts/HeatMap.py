import os

import matplotlib.lines as mlines
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from utils import Log

from mm.monitoring.CompareManifesto import CompareManifesto
from mm.monitoring.CompareThresholds import CompareThresholds

log = Log("HeatMap")


class HeatMap:

    ASPECT_RATIO = 16 / 9
    WIDTH = 1600
    HEIGHT = int(WIDTH / ASPECT_RATIO)
    CHART_PATH = os.path.join("images", "heat_map.png")

    def __init__(self):
        self.compare_manifesto = CompareManifesto()
        self.n_manifesto_items = self.compare_manifesto.n_manifesto_items
        self.overall_progress = self.compare_manifesto.get_overall_progress()

        self.n_x = (
            int((HeatMap.ASPECT_RATIO * self.n_manifesto_items) ** 0.5) + 1
        )
        self.n_y = int(self.n_manifesto_items / self.n_x) + 1

        dim = min(HeatMap.WIDTH / self.n_x, HeatMap.HEIGHT / self.n_y)
        self.x_dim = dim
        self.y_dim = dim

    @staticmethod
    def get_color(similarity):
        for group, min_similarity in CompareThresholds.THRESHOLDS.items():
            if similarity >= min_similarity:
                return CompareThresholds.COLORS[group]
        return CompareThresholds.COLORS["nil"]

    def draw_base_grid(self):

        ax = plt.gca()

        for i in range(self.n_x):
            for j in range(self.n_y):
                i_manifesto = i + j * self.n_x
                if i_manifesto >= self.n_manifesto_items:
                    continue
                square = patches.Rectangle(
                    (i * self.x_dim, j * self.y_dim),
                    self.x_dim,
                    self.y_dim,
                    edgecolor="lightgrey",
                    facecolor="white",
                )
                ax.add_patch(square)

    def draw_match_grid(self):
        ax = plt.gca()
        similarity_data_list = (
            self.compare_manifesto.get_similarity_data_list()
        )
        for d in similarity_data_list:
            i = d["i"]
            similarity = d["similarity"]
            color = HeatMap.get_color(similarity)
            i_display = i % self.n_x
            j_display = i // self.n_x

            square = patches.Rectangle(
                (i_display * self.x_dim, j_display * self.y_dim),
                self.x_dim,
                self.y_dim,
                edgecolor="#eee",
                facecolor=color,
            )
            ax.add_patch(square)

    def draw_legend(self):
        ax = plt.gca()

        handles = []
        for group, color in CompareThresholds.COLORS.items():
            if group == "nil":
                continue
            description = CompareThresholds.TEXTUAL[group]
            handles.append(
                mlines.Line2D(
                    [],
                    [],
                    color=color,
                    marker="s",
                    linestyle="None",
                    markersize=10,
                    label=description,
                )
            )

        ax.legend(
            handles=handles,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.1),
            ncol=4,
            frameon=False,
        )

    def draw(self):
        plt.close()
        plt.figure(figsize=(8, 4.5))
        ax = plt.gca()
        ax.set_aspect("equal")
        self.draw_base_grid()
        self.draw_match_grid()
        self.draw_legend()

        ax.set_xlim(0, self.n_x * self.x_dim)
        ax.set_ylim(0, self.n_y * self.y_dim)
        plt.gca().invert_yaxis()
        plt.axis("off")
        plt.title(
            "Manifesto Items vs. Cabinet Decisions"
            + f" (Progress: {self.overall_progress:.1%})",
            fontsize=12,
            pad=20,
        )
        plt.tight_layout()

        plt.savefig(HeatMap.CHART_PATH, dpi=300)
        plt.close()
        log.info(f"Wrote {HeatMap.CHART_PATH}.")
