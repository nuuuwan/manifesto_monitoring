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
            "This repository contains utility libraries & tools for"
            " tracking, analyzing, & visualizing the implementation of the"
            f" [2024 NPP manifesto]({self.SOURCE_URL}) —"
            " now the **de facto policy framework**"
            " of the 🇱🇰 Sri Lankan Government (2025).",
            "",
            "🛠️ Built for researchers, developers, journalists, & citizens"
            " who want **accountability & transparency** in governance.",
            "",
            "🔍 Use this repo to:",
            "",
            "- Track progress on key promises",
            "- Analyze policy implementation",
            "- Build visual dashboards & reports",
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

    # flake8: noqa: C901 - HACK!
    @cached_property
    def compare_summary_lines(self):

        data_list = CompareManifesto().high_similarity_pairs
        manifesto_idx = NPPManifestoPDF().get_manifesto().all_idx
        CabinetDecision.idx()
        manifesto_to_datalist = {x["manifesto_key"]: x for x in data_list}

        idx = {
            "all": {
                "l1": "-",
                "l1_topic": "all",
                "n": 0,
                "⚪ 0.5 - 0.6": 0,
                "🟡 0.6 - 0.7": 0,
                "🟢 0.7 < ": 0,
            }
        }
        for manifesto_key, manifesto in manifesto_idx.items():
            l1 = manifesto_key[:1]
            if l1 not in idx:
                idx[l1] = {
                    "l1": l1,
                    "l1_topic": manifesto["l1_topic"],
                    "n": 0,
                    "⚪ 0.5 - 0.6": 0,
                    "🟡 0.6 - 0.7": 0,
                    "🟢 0.7 < ": 0,
                }

            for k in ["all", l1]:
                idx[k]["n"] += 1
                sim_data = manifesto_to_datalist.get(manifesto_key)
                if sim_data:
                    similarity = sim_data["similarity"]
                    if similarity > 0.7:
                        idx[k]["🟢 0.7 < "] += 1
                    elif similarity > 0.6:
                        idx[k]["🟡 0.6 - 0.7"] += 1
                    else:
                        idx[k]["⚪ 0.5 - 0.6"] += 1

        d_list = [x[1] for x in sorted(list(idx.items()), key=lambda x: x[0])]

        new_d_list = []
        for d in d_list:

            def f(x):
                p = d[x] / d["n"]
                return f"{p:.0%}"

            new_d_list.append(
                {
                    "l1": d["l1"],
                    "l1_topic": d["l1_topic"],
                    "n": d["n"],
                    "⚪ 0.5 - 0.6": f("⚪ 0.5 - 0.6"),
                    "🟡 0.6 - 0.7": f("🟡 0.6 - 0.7"),
                    "🟢 0.7 < ": f("🟢 0.7 < "),
                }
            )

        return [
            "### Summary",
            "",
            self.build_markdown_table(new_d_list),
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
            emoji = "🟢"
        elif similarity >= 0.6:
            emoji = "🟡"
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
                "## 🤖 AI Comparison of NPP Manifesto Promises & Cabinet Decisions",
                "",
                "This section compares the NPP manifesto promises with"
                " Cabinet Decisions,"
                " using OpenAI's"
                f" [{
                    EmbeddingStore.MODEL}]({
                    EmbeddingStore.MODEL_URL}) Model.",
                "",
            ]
            + self.compare_summary_lines
            + self.compare_detail_lines
        )

    @cached_property
    def lines(self):
        return self.header_lines + self.compare_lines

    def build(self):
        File(self.README_PATH).write_lines(self.lines)
        log.info(f"Wrote {self.README_PATH} ({len(self.lines)} lines)")
