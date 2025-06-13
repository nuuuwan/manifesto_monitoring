from dataclasses import dataclass
from functools import cached_property
from mm.manifesto.comps.L2Topic import L2Topic
import re


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

    def to_dict(self):
        return dict(
            l1_num=self.l1_num,
            title=self.title,
            l2_topics=[l2_topic.to_dict() for l2_topic in self.l2_topics],
        )

    @cached_property
    def short_title(self):
        return f'{self.l1_num}) {self.title}'

    def to_short_dict(self):
        return {
            l2_topic.short_title: l2_topic.to_short_dict()
            for l2_topic in self.l2_topics
        }
