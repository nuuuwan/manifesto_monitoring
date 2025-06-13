from dataclasses import dataclass
from mm.manifesto.comps import L1Topic


@dataclass
class NPPManifesto:
    l1_topics: list[L1Topic]

    def to_dict(self):
        return dict(
            l1_topics=[l1_topic.to_dict() for l1_topic in self.l1_topics]
        )

    def to_short_dict(self):
        return {
            l1_topic.short_title: l1_topic.to_short_dict()
            for l1_topic in self.l1_topics
        }
