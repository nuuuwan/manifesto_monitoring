from dataclasses import dataclass


@dataclass
class Introduction:
    introduction_lines: list[str]

    @staticmethod
    def from_lines(lines: list[str]) -> list[str]:
        introduction_lines = []
        for line in lines:
            if line == "Introduction":
                continue

            if line.endswith("Principles"):
                break

            introduction_lines.append(line)

        return Introduction(introduction_lines)

    def to_dict(self):
        return self.introduction_lines

    def to_md_lines(self):
        lines = []
        lines.append("#### Introduction")
        lines.extend(self.introduction_lines)
        return lines
