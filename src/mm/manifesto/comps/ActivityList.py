import re
from dataclasses import dataclass

from mm.manifesto.comps.Activity import Activity


@dataclass
class ActivityList:
    activities: list["Activity"]

    @staticmethod
    def __is_activity_title__(line):
        return (
            line.strip()
            and line[:2] != "■ "
            and len(line) < 64
            and not line[0].islower()
            and line[-1] != "."
            and line not in ["Childhood Development Centres"]  # HACK!
        )

    @staticmethod
    def from_lines(lines: list[str], l1_num, l2_num) -> list["Activity"]:
        activities = {}
        has_started = False
        for line in lines:

            if line.endswith("ACTIVITIES"):
                has_started = True
                continue

            if not has_started:
                continue

            line = re.sub(r"^\d+\.?\s*", "", line)

            if ActivityList.__is_activity_title__(line):
                activities[line] = []
            else:
                clean_line = line.strip()

                if line[:2] == "■ ":
                    clean_line = clean_line[2:].strip()
                    to_previous = False
                else:
                    clean_line = clean_line.strip()
                    to_previous = True

                if activities.keys():
                    last_activity = list(activities.keys())[-1]

                    if to_previous:
                        if activities[last_activity]:
                            activities[last_activity][-1] += " " + clean_line
                    else:
                        activities[last_activity].append(clean_line)

        return ActivityList(
            [
                Activity(
                    l1_num=l1_num,
                    l2_num=l2_num,
                    activity_num=activity_num,
                    title=title,
                    activity_items=items,
                )
                for activity_num, (title, items) in enumerate(
                    activities.items(), start=1
                )
            ]
        )

    def to_dense_dict(self):
        return {
            activity.title: activity.activity_items
            for activity in self.activities
        }

    def to_md_lines(self):
        lines = ["#### Activities"]
        for activity in self.activities:
            lines.extend(activity.to_md_lines())
        return lines
