import re
from dataclasses import dataclass


@dataclass
class Activity:
    l1_num: int
    l2_num: int
    activity_num: int
    title: str
    activity_items: list[str]

    @staticmethod
    def __is_activity_title__(line):
        if not line.strip():
            return False

        if line[:2] == "■ ":
            return False

        if (
            len(line) > 64
            or line[0].lower() == line[0]
            or line[-1] == "."
            or line in ["Childhood Development Centres"]  # HACK!
        ):
            return False

        return True

    @staticmethod
    def list_from_lines(lines: list[str], l1_num, l2_num) -> list["Activity"]:
        activities = {}
        has_started = False
        for line in lines:

            if line.endswith("ACTIVITIES"):
                has_started = True
                continue

            if not has_started:
                continue

            line = re.sub(r"^\d+\.?\s*", "", line)

            if Activity.__is_activity_title__(line):
                activities[line] = []
            else:
                clean_line = line.strip()
                clean_line = clean_line.replace("■ ", "")
                clean_line = clean_line.replace("Y ear", "Year")  # HACK!
                if activities.keys():
                    last_activity = list(activities.keys())[-1]
                    activities[last_activity].append(clean_line)

        return [
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

    def to_dict(self):
        return {
            "title": self.title,
            "activity_items": self.activity_items,
        }

    def to_md_lines(self):
        lines = [
            "##### "
            + f"{self.l1_num:01d}.{self.l2_num:02d}.A{self.activity_num:02d})"
            + f" {self.title}"
        ]
        if self.activity_items:
            for item in self.activity_items:
                lines.append(f"- {item}")
        return lines

    def __len__(self):
        return len(self.activity_items)
