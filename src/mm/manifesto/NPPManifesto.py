from dataclasses import dataclass

from mm.manifesto.comps import L1Topic
from mm.manifesto.NPPManifestoDB import NPPManifestoDB


@dataclass
class NPPManifesto(NPPManifestoDB):
    l1_topics: list[L1Topic]

    def to_dense_dict(self):
        return {
            l1_topic.short_title: l1_topic.to_dense_dict()
            for l1_topic in self.l1_topics
        }

    def to_md_lines(self):
        lines = ["# NPP Manifesto"]
        for l1_topic in self.l1_topics:
            lines.extend(l1_topic.to_md_lines())
        return lines
