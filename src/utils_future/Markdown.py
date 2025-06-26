class Markdown:

    @staticmethod
    def __get_header_cells__(col: str) -> str:
        if col in [
            "Manifesto",
            "Cabinet Decision (Best Match)",
            "l1_topic",
            "Group",
        ]:
            return ":--"
        return "--:"

    @staticmethod
    def build_markdown_table(data_list: list[dict]) -> str:
        header = list(data_list[0].keys())
        header_row = " | ".join(header)
        separator_row = " | ".join(
            [Markdown.__get_header_cells__(col) for col in header]
        )
        data_rows = "\n".join(
            " | ".join(str(row[col]) for col in header) for row in data_list
        )

        return f"{header_row}\n{separator_row}\n{data_rows}"
