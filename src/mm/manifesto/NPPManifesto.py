from dataclasses import dataclass

from mm.manifesto.comps import L1Topic
from mm.manifesto.NPPManifestoDB import NPPManifestoDB


@dataclass
class NPPManifesto(NPPManifestoDB):
    l1_topics: list[L1Topic]

    SOURCE_URL = "https://www.npp.lk/up/policies/en/npppolicystatement.pdf"

    def to_dense_dict(self):
        return {
            l1_topic.short_title: l1_topic.to_dense_dict()
            for l1_topic in self.l1_topics
        }

    def to_md_lines(self):
        lines = [
            "# NPP Manifesto",
            f"Source: [{self.SOURCE_URL}]({self.SOURCE_URL})",
        ]
        for l1_topic in self.l1_topics:
            lines.extend(l1_topic.to_md_lines())
        return lines
