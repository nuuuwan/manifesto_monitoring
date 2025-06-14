from dataclasses import dataclass
from functools import cached_property

from mm.manifesto.comps.Principle import Principle


@dataclass
class Introduction:
    l1_num: int
    l2_num: int
    introduction_lines: list[str]

    @staticmethod
    def __get_introduction_lines__(lines: list[str]) -> list[str]:
        introduction_lines = []
        has_started = False
        for line in lines:
            if line == "Introduction":
                has_started = True
                continue
            if not has_started:
                continue
            if Principle.is_principle_title_text(line):
                break

            introduction_lines.append(line.strip())
        return introduction_lines

    @staticmethod
    def __compress_introduction_lines__(lines: list[str]) -> list[str]:
        compressed_lines = []
        for line in lines:
            if not line:
                continue
            if not line[0].isupper():
                compressed_lines[-1] += " " + line.strip()
            else:
                compressed_lines.append(line.strip())
        return compressed_lines

    @staticmethod
    def from_lines(lines: list[str], l1_num: int, l2_num: int) -> list[str]:
        introduction_lines = Introduction.__get_introduction_lines__(lines)

        compressed_introdiction_lines = (
            Introduction.__compress_introduction_lines__(introduction_lines)
        )

        return Introduction(l1_num, l2_num, compressed_introdiction_lines)

    @cached_property
    def key(self):
        return f"{self.l1_num:01d}.{self.l2_num:02d}"

    def to_md_lines(self):
        lines = []
        lines.append(f"#### Introduction [{self.key}]")
        lines.extend(self.introduction_lines)
        return lines
