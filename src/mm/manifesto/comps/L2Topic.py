from dataclasses import dataclass
from functools import cached_property
import re


@dataclass
class L2Topic:
    l1_num: int
    l2_num: int
    title: str
    introduction_lines: list[str]
    principles: list[str]
    activities: list[str]

    @staticmethod
    def __extract_introduction__(lines: list[str]) -> list[str]:
        introduction_lines = []
        for line in lines:
            if line == "Introduction":
                continue

            if line.endswith("Principles"):
                break

            introduction_lines.append(line)

        return introduction_lines

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
        if line[:2] == '■ ':
            return False

        if (
            len(line) > 64
            or line[0].lower() == line[0]
            or line[-1] == '.'
            or line in ['Childhood Development Centres']  # HACK!
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
                last_activity = list(activities.keys())[-1]
                activities[last_activity].append(clean_line)

        return activities

    @staticmethod
    def from_lines(lines: list[str]) -> "L2Topic":
        return L2Topic(
            introduction_lines=L2Topic.__extract_introduction__(lines),
            principles=L2Topic.__extract_principles__(lines),
            activities=L2Topic.__extract_activities__(lines),
        )

    @staticmethod
    def from_line(line):
        pattern = r'^\s*(\d+)\.(\d+)\.?\s+(.*?)\s+(\d+)\s*$'
        match = re.match(pattern, line)
        if not match:
            return None
        return L2Topic(
            l1_num=int(match.group(1)),
            l2_num=int(match.group(2)),
            title=match.group(3),
            introduction_lines=[],
            principles=[],
            activities=[],
        )

    def to_dict(self):
        return dict(
            l1_num=self.l1_num,
            l2_num=self.l2_num,
            title=self.title,
            introduction_lines=self.introduction_lines,
            principles=self.principles,
            activities=self.activities,
        )

    @cached_property
    def short_title(self):
        return f'{self.l1_num:01d}.{self.l2_num:02d}) {self.title}'

    def to_short_dict(self):
        return {}
