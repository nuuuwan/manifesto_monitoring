from dataclasses import dataclass


@dataclass
class Introduction:
    introduction_lines: list[str]

    @staticmethod
    def from_lines(lines: list[str]) -> list[str]:
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

            introduction_lines.append(line)

        compressed_introdiction_lines = []
        for line in introduction_lines:
            if not line:
                continue
            if line[0].islower():
                compressed_introdiction_lines[-1] += " " + line.strip()
            else:
                compressed_introdiction_lines.append(line.strip())

        return Introduction(compressed_introdiction_lines)

    def to_dict(self):
        return self.introduction_lines

    def to_md_lines(self):
        lines = []
        lines.append("#### Introduction")
        lines.extend(self.introduction_lines)
        return lines
