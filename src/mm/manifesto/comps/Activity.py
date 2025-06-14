from dataclasses import dataclass
from functools import cached_property


@dataclass
class Activity:
    l1_num: int
    l2_num: int
    activity_num: int
    title: str
    activity_items: list[str]

    NO_TITLE = "NO-TITLE"

    @cached_property
    def n_items(self) -> int:
        return len(self.activity_items)

    @staticmethod
    def is_activity_title_text(line: str) -> bool:
        return (
            line.endswith("ACTIVITIES")
            or line.endswith("ACTIONS")
            or line.endswith("Activities")
        )

    def to_dense_dict(self):
        return {self.title: self.activity_items}

    def __len__(self):
        return len(self.activity_items)

    @property
    def key(self):
        return f"{self.l1_num:01d}.{self.l2_num:02d}.A{self.activity_num:02d}"

    def to_dict(self):
        return {
            "key": self.key,
            "l1_num": self.l1_num,
            "l2_num": self.l2_num,
            "activity_num": self.activity_num,
            "title": self.title,
            "n_items": len(self),
        }

    def to_md_lines(self):
        lines = ["##### " + f"{self.key})" + f" {self.title}"]
        if self.activity_items:
            for i_item, item in enumerate(self.activity_items, start=1):
                lines.append(f"- {self.key}.{i_item:02d}) {item}")
        return lines
