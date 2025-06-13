from dataclasses import dataclass


@dataclass
class L2Chapter:
    introduction_lines: list[str]
    principles: list[str]

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
    def from_lines(lines: list[str]) -> "L2Chapter":
        return L2Chapter(
            introduction_lines=L2Chapter.__extract_introduction__(lines),
            principles=L2Chapter.__extract_principles__(lines),
        )
