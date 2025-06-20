import re
from dataclasses import dataclass
from functools import cached_property

from mm.manifesto.comps.Activity import Activity
from mm.manifesto.comps.Common import Common


@dataclass
class ActivityList:
    l1_num: int
    l2_num: int
    activities: list["Activity"]

    @staticmethod
    def __is_activity_title__(line):

        # HACK
        for k in [
            "earners",
            "families and women affected by Gender-based/intimate partner",
            "violence.",
            "and Innovation)",
            "developing fisheries harbours",
            "transportation, tourism, and other industries",
            "studies",
            "economic development",
            "improvements to required infrastructure",
        ]:
            if line == k:
                return True

        return (
            line.strip()
            and not Common.is_bullet(line)
            and len(line) < 64
            and not line[0].islower()
            and line[-1] != "."
            and line
            not in [
                "Childhood Development Centres",
                "Power",
                "02. An honourable life",
                "An honourable life",
                "A safe country",
                "03. A modern life",
                "A modern life",
                "A wealthy nation",
                "04. A dignified life",
                "A dignified life",
                "A strong country",
            ]  # HACK!
        )

    @staticmethod
    def __get_activities_lines__(lines: list[str]) -> list[str]:
        activities_lines = []
        has_started = False
        for line in lines:
            if Activity.is_activity_title_text(line):
                has_started = True
                continue
            if not has_started:
                continue
            line = re.sub(r"^\d+\.?\s*", "", line)
            line = line.strip()
            activities_lines.append(line)
        return activities_lines

    @staticmethod
    def __parse_activity_line__(line: str, activities) -> str:
        is_bullet = Common.is_bullet(line)
        line = line[2:].strip() if is_bullet else line.strip()

        if not activities:
            if is_bullet:
                activities[Activity.NO_TITLE] = [line]
            return activities

        last_activity = list(activities.keys())[-1]
        if is_bullet:
            activities[last_activity].append(line)
        elif activities[last_activity]:
            activities[last_activity][-1] += " " + line
        else:
            activities[last_activity].append(line)

        return activities

    @staticmethod
    def __get_activities_from_lines__(lines: list[str]) -> list[str]:
        activities_lines = ActivityList.__get_activities_lines__(lines)
        activities = {}
        for line in activities_lines:

            # flake8: noqa: F401
            if ActivityList.__is_activity_title__(line):

                last_key = list(activities.keys())[-1] if activities else None
                if last_key:
                    if activities[last_key]:
                        activities[line] = []
                    else:
                        new_key = last_key + " " + line
                        activities[new_key] = []
                        del activities[last_key]
                else:
                    activities[line] = []
                continue

            activities = ActivityList.__parse_activity_line__(
                line, activities
            )

        return activities

    @staticmethod
    def from_lines(lines: list[str], l1_num, l2_num) -> list["Activity"]:
        activities = ActivityList.__get_activities_from_lines__(lines)
        return ActivityList(
            l1_num=l1_num,
            l2_num=l2_num,
            activities=[
                Activity(
                    l1_num=l1_num,
                    l2_num=l2_num,
                    activity_num=activity_num,
                    title=title.strip(),
                    activity_items=[item.strip() for item in items],
                )
                for activity_num, (title, items) in enumerate(
                    activities.items(), start=1
                )
            ],
        )

    def to_dense_dict(self):
        return {
            activity.title: activity.activity_items
            for activity in self.activities
        }

    @cached_property
    def key(self):
        return f"{self.l1_num:01d}.{self.l2_num:02d}"

    def to_md_lines(self):
        lines = [f"#### Activities [{self.key}]"]
        for activity in self.activities:
            lines.extend(activity.to_md_lines())
        return lines

    def __len__(self):
        return len(self.activities)
