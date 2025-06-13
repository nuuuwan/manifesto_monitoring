from dataclasses import dataclass
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
