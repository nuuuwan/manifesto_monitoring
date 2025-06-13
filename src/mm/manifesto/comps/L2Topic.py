import re
from dataclasses import dataclass
from functools import cached_property

from utils import Log

from mm.manifesto.comps.Introduction import Introduction

log = Log("L2Topic")


@dataclass
class L2Topic:
    l1_num: int
    l2_num: int
    title: str
    introduction: Introduction
    principles: list[str]
    activities: list[str]

    @property
    def n_principles(self) -> int:
        return len(self.principles)

    @property
    def n_activities(self) -> int:
        return len(self.activities)

    @classmethod
    def __extract_principles__(cls, lines: list[str]) -> list[str]:
        principles = []
        has_started = False
        for line in lines:
            if line.endswith("Principles"):
                has_started = True
                continue
            if line.endswith("ACTIVITIES"):
                break

            if has_started:
                principles.append(line[2:].strip())

        return principles

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
    def __extract_activities__(lines: list[str]) -> list[str]:

        activities = {}
        has_started = False
        for line in lines:

            if line.endswith("ACTIVITIES"):
                has_started = True
                continue

            if not has_started:
                continue

            # remove digits from beginning of the line with re
            line = re.sub(r"^\d+\.?\s*", "", line)

            if L2Topic.__is_activity_title__(line):
                activities[line] = []
            else:
                clean_line = line.strip()
                clean_line = clean_line.replace("■ ", "")
                clean_line = clean_line.replace("Y ear", "Year")  # HACK!
                if activities.keys():
                    last_activity = list(activities.keys())[-1]
                    activities[last_activity].append(clean_line)

        return activities

    def expand_fields_from_lines(self, lines: list[str]) -> "L2Topic":
        self.introduction = Introduction.from_lines(lines)
        self.principles = L2Topic.__extract_principles__(lines)
        self.activities = L2Topic.__extract_activities__(lines)
        log.debug(
            f"[{self.short_title}] n_principles={self.n_principles}, "
            + f"n_activities={self.n_activities} activities"
        )

        return self

    @staticmethod
    def from_line(line):
        pattern = r"^\s*(\d+)\.(\d+)\.?\s+(.*?)\s+(\d+)\s*$"
        match = re.match(pattern, line)
        if not match:
            return None
        return L2Topic(
            l1_num=int(match.group(1)),
            l2_num=int(match.group(2)),
            title=match.group(3),
            introduction=[],
            principles=[],
            activities=[],
        )

    def to_dict(self):
        return dict(
            l1_num=self.l1_num,
            l2_num=self.l2_num,
            title=self.title,
            introduction=self.introduction.introduction_lines,
            principles=self.principles,
            activities=self.activities,
        )

    @cached_property
    def short_title(self):
        return f"{self.l1_num:01d}.{self.l2_num:02d}) {self.title}"

    def to_dense_dict(self):
        return {}

    def to_md_lines(self):
        lines = [f"### {self.short_title}"]
        if self.introduction:
            lines.extend(self.introduction.to_md_lines())
        if self.principles:
            lines.append("#### Principles")
            for principle in self.principles:
                lines.append(f"- {principle}")
        if self.activities:
            lines.append("#### Activities")
            for activity, details in self.activities.items():
                lines.append(f"- {activity}")
                for detail in details:
                    lines.append(f"  - {detail}")
        return lines
