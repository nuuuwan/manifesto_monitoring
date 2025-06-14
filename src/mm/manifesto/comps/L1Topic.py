import re
from dataclasses import dataclass
from functools import cached_property

from mm.manifesto.comps.L2Topic import L2Topic


@dataclass
class L1Topic:
    l1_num: int
    title: str
    l2_topics: list[L2Topic]

    @staticmethod
    def from_line(line):
        pattern = r"^(?:(\d+)\s+)?(\d+)\.\s+(.*)$"
        match = re.match(pattern, line)
        if not match:
            return None

        return L1Topic(
            l1_num=int(match.group(2)),
            title=match.group(3),
            l2_topics=[],
        )

    @cached_property
    def short_title(self):
        return f"{self.l1_num}) {self.title}"

    def to_dict(self):
        return {
            "l1_num": self.l1_num,
            "title": self.title,
            "n_l2_topics": len(self.l2_topics),
        }

    def to_dense_dict(self):
        return {
            l2_topic.short_title: l2_topic.to_dense_dict()
            for l2_topic in self.l2_topics
        }

    def to_md_lines(self):
        lines = [f"## {self.short_title}"]
        for l2_topic in self.l2_topics:
            lines.extend(l2_topic.to_md_lines())
        return lines
