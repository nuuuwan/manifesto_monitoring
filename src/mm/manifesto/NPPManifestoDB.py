from functools import cached_property


class NPPManifestoDB:
    @cached_property
    def l1_topics_table(self):
        return [l1_topic.to_dict() for l1_topic in self.l1_topics]

    @cached_property
    def l2_topics_table(self):
        table = []
        for l1_topic in self.l1_topics:
            for l2_topic in l1_topic.l2_topics:
                table.append(l2_topic.to_dict())
        return table

    @cached_property
    def activities_table(self):
        table = []
        for l1_topic in self.l1_topics:
            for l2_topic in l1_topic.l2_topics:
                activity_list = l2_topic.activity_list
                for activity in activity_list.activities:
                    table.append(activity.to_dict())
        return table
