from dataclasses import dataclass


@dataclass
class Principles:
    l1_num: int
    l2_num: int
    principles: list[str]

    def __len__(self):
        return len(self.principles)

    @staticmethod
    def from_lines(lines: list[str], l1_num, l2_num) -> "Principles":
        principles = []
        has_started = False
        for line in lines:
            if line.endswith("Principles"):
                has_started = True
                continue
            if line.endswith("ACTIVITIES"):
                break

            if has_started:
                if line[:2] == "■ ":
                    principles.append(line[2:].strip())
                else:
                    if principles:
                        principles[-1] += " " + line.strip()

        return Principles(l1_num, l2_num, principles)

    def to_dict(self):
        return self.principles

    def to_md_lines(self):
        lines = []
        lines.append("#### Principles")
        for i_principle, principle in enumerate(self.principles, start=1):
            principle = f"P{i_principle}) {principle}"
            principle = f"{self.l1_num}.{self.l2_num:02d}.{principle}"
            lines.append(f"- {principle}")
        return lines
