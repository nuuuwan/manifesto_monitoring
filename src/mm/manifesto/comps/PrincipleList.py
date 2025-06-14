from dataclasses import dataclass
from functools import cached_property

from mm.manifesto.comps.Principle import Principle


@dataclass
class PrincipleList:
    l1_num: int
    l2_num: int
    principles: list[Principle]

    def __len__(self):
        return len(self.principles)

    @staticmethod
    def __get_principles_lines__(lines: list[str]) -> list[str]:
        principles_lines = []
        has_started = False
        for line in lines:
            if line.endswith("Principles"):
                has_started = True
                continue
            if line.endswith("ACTIVITIES"):
                break

            if has_started:
                principles_lines.append(line.strip())
        return principles_lines

    @staticmethod
    def from_lines(lines: list[str], l1_num, l2_num) -> "PrincipleList":
        principles = []
        principles_num = 0

        principle_lines = PrincipleList.__get_principles_lines__(lines)
        for line in principle_lines:

            if line[:2] == "■ ":
                principles_num += 1
                principles.append(
                    Principle(
                        l1_num=l1_num,
                        l2_num=l2_num,
                        principle_num=principles_num,
                        title=line[2:].strip(),
                    )
                )
            elif principles:
                principles[-1].title += " " + line.strip()

        return PrincipleList(l1_num, l2_num, principles)

    @cached_property
    def key(self):
        return f"{self.l1_num:01d}.{self.l2_num:02d}"

    def to_md_lines(self):
        lines = []
        lines.append(f"#### Principles [{self.key}]")
        lines.extend([p.to_md_line() for p in self.principles])
        return lines
