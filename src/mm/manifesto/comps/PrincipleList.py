from dataclasses import dataclass

from mm.manifesto.comps.Principle import Principle


@dataclass
class PrincipleList:
    l1_num: int
    l2_num: int
    principles: list[Principle]

    def __len__(self):
        return len(self.principles)

    @staticmethod
    def from_lines(lines: list[str], l1_num, l2_num) -> "PrincipleList":
        principles = []
        principles_num = 0
        has_started = False
        for line in lines:
            if line.endswith("Principles"):
                has_started = True
                continue
            if line.endswith("ACTIVITIES"):
                break

            if has_started:
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
                else:
                    if principles:
                        principles[-1].title += " " + line.strip()

        return PrincipleList(l1_num, l2_num, principles)

    def to_md_lines(self):
        lines = []
        lines.append("#### Principles")
        lines.extend([p.to_md_line() for p in self.principles])
        return lines
