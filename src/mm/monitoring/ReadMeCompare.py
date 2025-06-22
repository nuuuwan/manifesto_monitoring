from functools import cached_property

from mm.ai import EmbeddingStore
from mm.monitoring.charts.HeatMap import HeatMap
from mm.monitoring.ReadMeCompareDetails import ReadMeCompareDetails
from mm.monitoring.ReadMeCompareSummary import ReadMeCompareSummary


class ReadMeCompare(ReadMeCompareDetails, ReadMeCompareSummary):
    @cached_property
    def heatmap_lines(self):
        HeatMap().draw()
        return [
            f"![{HeatMap.CHART_PATH}]({HeatMap.CHART_PATH})",
            "",
        ]

    @cached_property
    def compare_lines(self):
        n_manifesto_items = self.compare_manifesto.n_manifesto_items
        n_cabinet_decisions = self.compare_manifesto.n_cabinet_decisions

        return (
            [
                "## 🤖 AI Comparison of "
                f" {n_manifesto_items:,} NPP Manifesto Promises &"
                f" {n_cabinet_decisions:,} NPP Cabinet Decisions",
                "",
                "This section compares the NPP manifesto promises with"
                " Cabinet Decisions,"
                " using OpenAI's"
                f" [{
                    EmbeddingStore.MODEL}]({
                    EmbeddingStore.MODEL_URL}) Model.",
                "",
            ]
            + self.heatmap_lines
            + self.get_similarity_threshold_legend_lines()
            + self.compare_summary_lines
            + self.compare_detail_lines
        )
