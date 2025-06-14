from functools import cached_property


class NPPManifestoDB:
    @cached_property
    def l1_topics_table(self):
        return [l1_topic.to_dict() for l1_topic in self.l1_topics]
