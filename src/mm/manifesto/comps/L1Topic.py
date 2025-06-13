from dataclasses import dataclass
from manifesto.comps.L2Topic import L2Topic

@dataclass
class L1Topic:
    l2_topics: list[L2Topic]
