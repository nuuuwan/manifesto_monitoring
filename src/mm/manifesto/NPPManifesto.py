from dataclasses import dataclass
from mm.manifesto.comps import L1Topic


@dataclass
class NPPManifesto:
    l1_topics: list[L1Topic]
