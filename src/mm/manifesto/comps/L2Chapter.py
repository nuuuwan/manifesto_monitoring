from dataclasses import dataclass


@dataclass
class L2Chapter:
    introduction_lines: list[str]

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

    @staticmethod
    def from_lines(lines: list[str]) -> "L2Chapter":
        introduction_lines = L2Chapter.__extract_introduction__(lines)
        return L2Chapter(introduction_lines=introduction_lines)
