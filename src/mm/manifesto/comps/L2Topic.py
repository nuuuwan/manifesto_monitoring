import re
from dataclasses import dataclass
from functools import cached_property

from utils import Log

from mm.manifesto.comps.ActivityList import ActivityList
from mm.manifesto.comps.Introduction import Introduction
from mm.manifesto.comps.PrincipleList import PrincipleList

log = Log("L2Topic")


@dataclass
class L2Topic:
    l1_num: int
    l2_num: int
    title: str
    introduction: Introduction
    principle_list: PrincipleList
    activity_list: ActivityList

    @cached_property
    def n_principles(self):
        return len(self.principle_list)

    @cached_property
    def n_activities(self):
        return len(self.activity_list)

    def expand_fields_from_lines(self, lines: list[str]) -> "L2Topic":
        self.introduction = Introduction.from_lines(
            lines, l1_num=self.l1_num, l2_num=self.l2_num
        )
        self.principle_list = PrincipleList.from_lines(
            lines, l1_num=self.l1_num, l2_num=self.l2_num
        )
        self.activity_list = ActivityList.from_lines(
            lines, l1_num=self.l1_num, l2_num=self.l2_num
        )
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
            principle_list=None,
            activity_list=None,
        )

    @cached_property
    def key(self):
        return f"{self.l1_num:01d}.{self.l2_num:02d}"

    @cached_property
    def short_title(self):
        return f"{self.key}) {self.title}"

    def to_dict(self):
        return {
            "key": self.key,
            "l1_num": self.l1_num,
            "l2_num": self.l2_num,
            "title": self.title,
            "n_principles": self.n_principles,
            "n_activities": self.n_activities,
        }

    def to_dense_dict(self):
        return self.activity_list.to_dense_dict()

    def to_md_lines(self):
        lines = [f"### {self.short_title}"]
        if self.introduction:
            lines.extend(self.introduction.to_md_lines())
        if self.principle_list:
            lines.extend(self.principle_list.to_md_lines())
        if self.activity_list:
            lines.extend(self.activity_list.to_md_lines())
        return lines
