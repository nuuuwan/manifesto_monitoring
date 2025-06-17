from functools import cached_property

from utils import File, Log

from mm.ai import EmbeddingStore
from mm.cabinet_decisions import CabinetDecision
from mm.manifesto import NPPManifestoPDF
from mm.monitoring.CompareManifesto import CompareManifesto

log = Log("ReadMe")


class ReadMe:
    README_PATH = "README.md"
    SOURCE_URL = "https://www.npp.lk/up/policies/en/npppolicystatement.pdf"

    @cached_property
    def header_lines(self):
        return [
            "# 🇱🇰 Manifesto Monitoring",
            "",
            "This repository contains utility libraries and tools for"
            " tracking, analyzing, and visualizing the implementation of the"
            f" [2024 NPP manifesto]({self.SOURCE_URL}) —"
            " now the **de facto policy framework**"
            " of the 🇱🇰 Sri Lankan Government (2025).",
            "",
            "🛠️ Built for researchers, developers, journalists, and citizens"
            " who want **accountability and transparency** in governance.",
            "",
            "🔍 Use this repo to:",
            "",
            "- Track progress on key promises",
            "- Analyze policy implementation",
            "- Build visual dashboards and reports",
            "",
            "📢 Public Data. Share. Fork. Contribute.",
            "",
            f"NPP Manifesto Source: [{self.SOURCE_URL}]({self.SOURCE_URL})",
            "",
        ]

    @staticmethod
    def build_markdown_table(data_list: list[dict]) -> str:
        header = list(data_list[0].keys())
        header_row = " | ".join(header)
        separator_row = " | ".join(["---"] * len(header))
        data_rows = "\n".join(
            " | ".join(str(row[col]) for col in header) for row in data_list
        )

        return f"{header_row}\n{separator_row}\n{data_rows}"

    @cached_property
    def compare_summary_lines(self):
        return [
            "### Summary",
            "",
        ]

    @staticmethod
    def get_manifesto_markdown(manifesto):
        return " ".join(
            [
                f"`{manifesto["key"]}`",
                f"**{manifesto['activity']}** ",
                f"{manifesto["item"]}",
            ]
        )

    @staticmethod
    def get_cabinet_decision_markdown(cabinet_decision):
        return " ".join(
            [
                f"[{cabinet_decision.key}]({cabinet_decision.source_url})",
                f"**{cabinet_decision.title}**",
            ]
        )

    @staticmethod
    def get_similarity_markdown(similarity):
        emoji = "⚪"
        if similarity >= 0.7:
            emoji = "🟡"
        elif similarity >= 0.9:
            emoji = "🟢"
        return f"{emoji} {similarity:.2f}"

    @staticmethod
    def get_table_data(x, manifesto_idx, cabinet_decision_idx):
        manifesto = manifesto_idx[x["manifesto_key"]]
        cabinet_decision = cabinet_decision_idx[x["cabinet_decision_key"]]
        similarity = x["similarity"]
        return {
            "Manifesto": ReadMe.get_manifesto_markdown(manifesto),
            "Cabinet Decision": ReadMe.get_cabinet_decision_markdown(
                cabinet_decision,
            ),
            "Similarity": ReadMe.get_similarity_markdown(similarity),
        }

    @cached_property
    def compare_data_lines(self):
        data_list = CompareManifesto().high_similarity_pairs
        manifesto_idx = NPPManifestoPDF().get_manifesto().all_idx
        cabinet_decision_idx = CabinetDecision.idx()

        table_data_list = [
            self.get_table_data(x, manifesto_idx, cabinet_decision_idx)
            for x in data_list
        ]
        return [
            self.build_markdown_table(table_data_list),
        ]

    @cached_property
    def compare_detail_lines(self):
        return [
            "### Manifesto/Decision Pairs with Similarity >= 0.7",
            "",
        ] + self.compare_data_lines

    @cached_property
    def compare_lines(self):
        return (
            [
                "## Comparison of NPP Manifesto Promises and Cabinet Decisions",
                "",
                "This section compares the NPP manifesto promises with"
                " Cabinet Decisions,"
                " using OpenAI's"
                f" [{
                    EmbeddingStore.MODEL}]({
                    EmbeddingStore.MODEL_URL}) Model.",
                "",
                "### Manifesto/Decision Pairs with Similarity >= 0.5",
                "",
            ]
            + self.compare_summary_lines
            + self.compare_data_lines
        )

    @cached_property
    def lines(self):
        return self.header_lines + self.compare_lines

    def build(self):
        File(self.README_PATH).write_lines(self.lines)
        log.info(f"Wrote {self.README_PATH} ({len(self.lines)} lines)")
