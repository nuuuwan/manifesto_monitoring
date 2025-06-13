from dataclasses import dataclass
from mm.manifesto.comps import L1Topic


@dataclass
class NPPManifestoBase:
    l1_topics: list[L1Topic]
