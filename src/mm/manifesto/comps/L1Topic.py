from dataclasses import dataclass
from mm.manifesto.comps.L2Topic import L2Topic


@dataclass
class L1Topic:
    l1_num: int
    title: str
    l2_topics: list[L2Topic]
