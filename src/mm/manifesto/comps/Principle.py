from dataclasses import dataclass
from functools import cached_property


@dataclass
class Principle:
    l1_num: int
    l2_num: int
    principle_num: int
    title: str

    @staticmethod
    def is_principle_title_text(line: str) -> bool:
        line = line.strip()
        return (
            line.endswith("PRINCIPLES")
            or line.endswith("Principles")
            or line.endswith("Principles:")
            or line.endswith("The principles")
        )

    @cached_property
    def key(self):
        return f"{self.l1_num}.{self.l2_num:02d}.P{self.principle_num}"

    def to_dict(self):
        return {
            "key": self.key,
            "l1_num": self.l1_num,
            "l2_num": self.l2_num,
            "principle_num": self.principle_num,
            "title": self.title,
        }

    @cached_property
    def short_title(self):
        return f"{self.key}) {self.title}"

    def to_md_line(self):
        return f"- {self.short_title}"
