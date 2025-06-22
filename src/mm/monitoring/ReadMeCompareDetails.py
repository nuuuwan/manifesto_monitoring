from functools import cached_property

from mm.monitoring.CompareThresholds import CompareThresholds
from utils_future import Markdown


class ReadMeCompareDetails:
    MIN_SIMILARITY = 0.5

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
    def get_cd_markdown(cabinet_decision):
        # cd = cabinet decision
        return " ".join(
            [
                f"[{cabinet_decision.key}]({cabinet_decision.source_url})",
                f"**{cabinet_decision.title}**",
            ]
        )

    @staticmethod
    def get_compare_details_table_row_data(
        x, manifesto_idx, cabinet_decision_idx
    ):
        manifesto = manifesto_idx[x["manifesto_key"]]
        cabinet_decision = cabinet_decision_idx[x["cabinet_decision_key"]]
        similarity = x["similarity"]
        cd = ReadMeCompareDetails.get_cd_markdown(
            cabinet_decision,
        )
        return {
            "Manifesto": ReadMeCompareDetails.get_manifesto_markdown(
                manifesto
            ),
            "Cabinet Decision (Best Match)": cd,
            "Similarity": CompareThresholds.get_similarity_markdown(
                similarity
            ),
        }

    def get_compare_details_table_data(self):
        table_data_list = [
            self.get_compare_details_table_row_data(
                x, self.manifesto_idx, self.cabinet_decision_idx
            )
            for x in self.data_list
        ]

        table_data_list = [
            dict(row=x[0]) | x[1] for x in enumerate(table_data_list, start=1)
        ]
        return table_data_list

    def get_compare_details_table(self):

        return [
            Markdown.build_markdown_table(
                self.get_compare_details_table_data()
            ),
        ]

    @cached_property
    def compare_detail_lines(self):
        return [
            "### Manifesto Items with Best Matching Cabinet Decisions",
            "",
        ] + self.get_compare_details_table()
