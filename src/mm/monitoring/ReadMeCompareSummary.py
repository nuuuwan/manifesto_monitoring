from functools import cached_property

from utils_future import Markdown


class ReadMeCompareSummary:
    THRESHOLDS = {
        "high": 0.7,
        "medium": 0.6,
        "low": 0.5,
    }

    EMOJIS = {
        "high": "🔴",
        "medium": "🟠",
        "low": "🟢",
        "nil": "⚪️",
    }

    @staticmethod
    def get_group_to_n(old_d):
        group_to_n = {}
        for sim in old_d["sim_list"]:
            group = ReadMeCompareSummary.get_group(sim)
            group_to_n[group] = group_to_n.get(group, 0) + 1
        return group_to_n

    @staticmethod
    def get_sim_data_summary(old_d):
        group_to_n = ReadMeCompareSummary.get_group_to_n(old_d)
        n = old_d["n"]
        d = {
            "l1": old_d["l1"],
            "l1_topic": old_d["l1_topic"],
            "n": n,
        }
        for group in ReadMeCompareSummary.THRESHOLDS:
            n_group = group_to_n.get(group, 0)
            p_group = n_group / n
            formatted_data = (
                f"{n_group} ({p_group:.0%})" if n_group > 0 else "-"
            )
            d[ReadMeCompareSummary.get_group_title(group)] = formatted_data
        return d

    @staticmethod
    def get_similarity_threshold_legend_lines():
        d_list = []
        for group, threshold in ReadMeCompareSummary.THRESHOLDS.items():
            d_list.append(
                {
                    "Group": ReadMeCompareSummary.get_group_title(group),
                    "Threshold": f"{threshold:.0%}",
                }
            )
        return [Markdown.build_markdown_table(d_list), ""]

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
            new_d_list.append(ReadMeCompareSummary.get_sim_data_summary(d))

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
    def get_group_title(group):
        return f"{ReadMeCompareSummary.EMOJIS[group]} {group.capitalize()}"

    @staticmethod
    def get_group(similarity):
        for group, threshold in ReadMeCompareSummary.THRESHOLDS.items():
            if similarity >= threshold:
                return group
        raise ValueError(f"Invalid similarity value: {similarity}. ")
