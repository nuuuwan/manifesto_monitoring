from functools import cached_property


class NPPManifestoDB:
    @cached_property
    def l1_topics_table(self):
        return [l1_topic.to_dict() for l1_topic in self.l1_topics]

    @cached_property
    def l2_topics(self):
        l2_topics = []
        for l1_topic in self.l1_topics:
            l2_topics.extend(l1_topic.l2_topics)
        return l2_topics

    @cached_property
    def l2_topics_table(self):
        table = []
        for l2_topic in self.l2_topics:
            table.append(l2_topic.to_dict())
        return table

    @cached_property
    def activity_list(self):
        activities = []
        for l2_topic in self.l2_topics:
            activities.extend(l2_topic.activity_list.activities)
        return activities

    @cached_property
    def activities_table(self):
        table = []
        for activity in self.activity_list:
            table.append(activity.to_dict())
        return table

    @cached_property
    def principle_list(self):
        principles = []
        for l2_topic in self.l2_topics:
            principles.extend(l2_topic.principle_list)
        return principles

    @cached_property
    def principles_table(self):
        table = []
        for principle in self.principle_list:
            table.append(principle.to_dict())
        return table

    @cached_property
    def activity_items_table(self):
        table = []
        for activity in self.activity_list:
            for activity_item_num, item in enumerate(
                activity.activity_items, start=1
            ):
                key = f"{activity.key}.{activity_item_num:02d}"
                table.append(
                    {
                        "key": key,
                        "l1_num": activity.l1_num,
                        "l2_num": activity.l2_num,
                        "activity_num": activity.activity_num,
                        "activity_item_num": activity_item_num,
                        "item": item,
                    }
                )
        return table

    @cached_property
    def all_table(self):
        table = []
        for l1_topic in self.l1_topics:
            for l2_topic in l1_topic.l2_topics:
                for activity in l2_topic.activity_list.activities:
                    for activity_item_num, item in enumerate(
                        activity.activity_items, start=1
                    ):
                        key = f"{activity.key}.{activity_item_num:02d}"
                        table.append(
                            {
                                "key": key,
                                "l1_num": activity.l1_num,
                                "l2_num": activity.l2_num,
                                "activity_num": activity.activity_num,
                                "activity_item_num": activity_item_num,
                                "l1_topic": l1_topic.title,
                                "l2_topic": l2_topic.title,
                                "activity": activity.title,
                                "item": item,
                            }
                        )
        return table
