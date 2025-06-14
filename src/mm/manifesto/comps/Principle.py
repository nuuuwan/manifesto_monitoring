from dataclasses import dataclass
from functools import cached_property


@dataclass
class Principle:
    l1_num: int
    l2_num: int
    principle_num: int
    title: str

    @cached_property
    def key(self):
        return f"{self.l1_num}.{self.l2_num:02d}.{self.principle_num}"

    @cached_property
    def short_title(self):
        return f"{self.key}) {self.title}"

    def to_md_line(self):
        return f"- {self.short_title}"
