from functools import cached_property

from mm.ai import EmbeddingStore
from mm.monitoring.CompareManifesto import CompareManifesto
from mm.monitoring.ReadMeCompareDetails import ReadMeCompareDetails
from mm.monitoring.ReadMeCompareSummary import ReadMeCompareSummary


class ReadMeCompare(ReadMeCompareDetails, ReadMeCompareSummary):

    @cached_property
    def compare_lines(self):
        n_manifesto = len(CompareManifesto().manifesto_key_to_text)
        n_cabinet_decisions = len(
            CompareManifesto().cabinet_decisions_key_to_text
        )

        return (
            [
                "## 🤖 AI Comparison of "
                f" {n_manifesto:,} NPP Manifesto Promises &"
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
            + self.get_similarity_threshold_legend_lines()
            + self.compare_summary_lines
            + self.compare_detail_lines
        )
