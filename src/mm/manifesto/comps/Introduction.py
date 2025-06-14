from dataclasses import dataclass


@dataclass
class Introduction:
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
            if line.endswith("Principles"):
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
    def from_lines(lines: list[str]) -> list[str]:
        introduction_lines = Introduction.__get_introduction_lines__(lines)

        compressed_introdiction_lines = (
            Introduction.__compress_introduction_lines__(introduction_lines)
        )

        return Introduction(compressed_introdiction_lines)

    def to_md_lines(self):
        lines = []
        lines.append("#### Introduction")
        lines.extend(self.introduction_lines)
        return lines
