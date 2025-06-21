from functools import cached_property

from mm.ai import EmbeddingStore
from mm.monitoring.CompareManifesto import CompareManifesto
from utils_future import Markdown


class ReadMeCompare:
    @staticmethod
    def get_sim_data_summary(old_d):
        group_to_n = {}
        for sim in old_d["sim_list"]:
            group = ReadMeCompare.get_group(sim)
            group_to_n[group] = group_to_n.get(group, 0) + 1

        n = old_d["n"]
        d = {
            "l1": old_d["l1"],
            "l1_topic": old_d["l1_topic"],
            "n": n,
        }
        for group in ReadMeCompare.THRESHOLDS:
            n_group = group_to_n.get(group, 0)
            p_group = n_group / n
            formatted_data = (
                f"{n_group} ({p_group:.0%})" if n_group > 0 else "-"
            )
            d[ReadMeCompare.get_group_title(group)] = formatted_data
        return d

    @cached_property
    def summary_data(self):  # noqa: C901

        idx = {
            "all": {
                "l1": "all",
                "l1_topic": "all",
                "n": 0,
                "sim_list": [],
            }
        }
        for manifesto_key, manifesto in self.manifesto_idx.items():
            l1 = manifesto_key[:1]
            if l1 not in idx:
                idx[l1] = {
                    "l1": l1,
                    "l1_topic": manifesto["l1_topic"],
                    "n": 0,
                    "sim_list": [],
                }

            for k in ["all", l1]:
                idx[k]["n"] += 1
                sim_data = self.manifesto_to_datalist.get(manifesto_key)
                if not sim_data:
                    continue
                similarity = sim_data["similarity"]
                idx[k]["sim_list"].append(similarity)

        new_d_list = []
        for d in idx.values():
            new_d_list.append(ReadMeCompare.get_sim_data_summary(d))

        new_d_list.sort(key=lambda x: (x["l1"]))
        return new_d_list

    @cached_property
    def compare_summary_lines(self):
        return [
            "### Summary",
            "",
            Markdown.build_markdown_table(self.summary_data),
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

    THRESHOLDS = {
        "high": 0.7,
        "medium": 0.6,
        "low": 0.5,
    }

    EMOJIS = {
        "high": "🟢",
        "medium": "🟡",
        "low": "🟠",
        "nil": "🔴",
    }

    @staticmethod
    def get_group_title(group):
        return f"{ReadMeCompare.EMOJIS[group]} {group.capitalize()}"

    @staticmethod
    def get_group(similarity):
        for group, threshold in ReadMeCompare.THRESHOLDS.items():
            if similarity >= threshold:
                return group
        raise ValueError(f"Invalid similarity value: {similarity}. ")

    @staticmethod
    def get_similarity_threshold_legend_lines():
        d_list = []
        for group, threshold in ReadMeCompare.THRESHOLDS.items():
            d_list.append(
                {
                    "Group": ReadMeCompare.get_group_title(group),
                    "Threshold": f"{threshold:.0%}",
                }
            )
        return [Markdown.build_markdown_table(d_list), ""]

    @staticmethod
    def get_similarity_markdown(similarity):
        group = ReadMeCompare.get_group(similarity)
        emoji = ReadMeCompare.EMOJIS[group]
        return f"{emoji} {similarity:.0%}"

    @staticmethod
    def get_table_data(x, manifesto_idx, cabinet_decision_idx):
        manifesto = manifesto_idx[x["manifesto_key"]]
        cabinet_decision = cabinet_decision_idx[x["cabinet_decision_key"]]
        similarity = x["similarity"]
        return {
            "Manifesto": ReadMeCompare.get_manifesto_markdown(manifesto),
            "Cabinet Decision": ReadMeCompare.get_cabinet_decision_markdown(
                cabinet_decision,
            ),
            "Similarity": ReadMeCompare.get_similarity_markdown(similarity),
        }

    @cached_property
    def compare_data_lines(self):
        table_data_list = [
            self.get_table_data(
                x, self.manifesto_idx, self.cabinet_decision_idx
            )
            for x in self.data_list
        ]

        table_data_list.sort(key=lambda x: (x["Similarity"],), reverse=True)

        table_data_list = [
            dict(row=x[0]) | x[1] for x in enumerate(table_data_list, start=1)
        ]

        return [
            Markdown.build_markdown_table(table_data_list),
        ]

    @cached_property
    def compare_detail_lines(self):
        return [
            "### Manifesto/Decision Pairs with Similarity >= 0.5",
            "",
        ] + self.compare_data_lines

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
