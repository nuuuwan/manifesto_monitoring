import os

import matplotlib.lines as mlines
import matplotlib.patches as patches
import matplotlib.pyplot as plt

from mm.monitoring.CompareManifesto import CompareManifesto


class HeatMap:
    ASPECT_RATIO = 16 / 9
    WIDTH = 1600
    HEIGHT = int(WIDTH / ASPECT_RATIO)
    CHART_PATH = os.path.join("images", "heat_map.png")

    def __init__(self):
        self.compare_manifesto = CompareManifesto()
        self.n_manifesto_items = self.compare_manifesto.n_manifesto_items

        self.n_x = (
            int((HeatMap.ASPECT_RATIO * self.n_manifesto_items) ** 0.5) + 1
        )
        self.n_y = int(self.n_manifesto_items / self.n_x) + 1
        self.x_dim = HeatMap.WIDTH / self.n_x
        self.y_dim = HeatMap.HEIGHT / self.n_y

    @staticmethod
    def get_color(similarity):  # noqa: CFQ004

        if similarity > 0.7:
            return "#f00"
        if similarity > 0.6:
            return "#f80"
        if similarity > 0.5:
            return "#0c0"
        return "#eee"

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
        similarity_data_list = self.compare_manifesto.similarity_data_list
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
                edgecolor="none",
                facecolor=color,
            )
            ax.add_patch(square)

    def draw_legend(self):
        ax = plt.gca()

        handles = []
        for color, label in [
            ("#f00", ">70% match"),
            ("#f80", "60–70% match"),
            ("#0c0", "50–60% match"),
        ]:
            handles.append(
                mlines.Line2D(
                    [],
                    [],
                    color=color,
                    marker="s",
                    linestyle="None",
                    markersize=10,
                    label=label,
                )
            )

        ax.legend(
            handles=handles,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.05),
            ncol=4,
            frameon=False,
        )

    def draw(self):
        plt.close()
        ax = plt.gca()
        self.draw_base_grid()
        self.draw_match_grid()
        self.draw_legend()

        padding = 100
        ax.set_xlim(0, self.n_x * self.x_dim + padding)
        ax.set_ylim(0, self.n_y * self.y_dim + padding)
        plt.gca().invert_yaxis()
        plt.axis("off")
        plt.title(
            "Manifesto Items with Cabinet Decisions Match",
            fontsize=16,
            pad=20,
        )
        plt.tight_layout()

        plt.savefig(HeatMap.CHART_PATH, dpi=300)
