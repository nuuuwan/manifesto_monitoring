import re
from dataclasses import dataclass
from functools import cached_property

from utils import Log

from mm.manifesto.comps.Activity import Activity
from mm.manifesto.comps.Introduction import Introduction
from mm.manifesto.comps.Principles import Principles

log = Log("L2Topic")


@dataclass
class L2Topic:
    l1_num: int
    l2_num: int
    title: str
    introduction: Introduction
    principles: Principles
    activities: list[Activity]

    def expand_fields_from_lines(self, lines: list[str]) -> "L2Topic":
        self.introduction = Introduction.from_lines(lines)
        self.principles = Principles.from_lines(lines)
        self.activities = Activity.list_from_lines(lines)
        return self

    @staticmethod
    def from_line(line):
        pattern = r"^\s*(\d+)\.(\d+)\.?\s+(.*?)\s+(\d+)\s*$"
        match = re.match(pattern, line)
        if not match:
            return None
        return L2Topic(
            l1_num=int(match.group(1)),
            l2_num=int(match.group(2)),
            title=match.group(3),
            introduction=None,
            principles=None,
            activities=[],
        )

    def to_dict(self):
        return dict(
            l1_num=self.l1_num,
            l2_num=self.l2_num,
            title=self.title,
            introduction=self.introduction.to_dict(),
            principles=self.principles.to_dict(),
            activities=[activity.to_dict() for activity in self.activities],
        )

    @cached_property
    def short_title(self):
        return f"{self.l1_num:01d}.{self.l2_num:02d}) {self.title}"

    def to_dense_dict(self):
        return {}

    def to_md_lines(self):
        lines = [f"### {self.short_title}"]
        if self.introduction:
            lines.extend(self.introduction.to_md_lines())
        if self.principles:
            lines.extend(self.principles.to_md_lines())
        if self.activities:
            lines.append("#### Activities")
            for activity in self.activities:
                lines.extend(activity.to_md_lines())
        return lines
