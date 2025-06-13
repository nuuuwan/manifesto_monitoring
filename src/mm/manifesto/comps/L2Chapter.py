from dataclasses import dataclass


@dataclass
class L2Chapter:
    introduction_lines: list[str]

    @staticmethod
    def from_lines(lines: list[str]) -> "L2Chapter":
        pass
