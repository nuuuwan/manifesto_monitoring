from dataclasses import dataclass


@dataclass
class Principles:
    principles: list[str]

    def __len__(self):
        return len(self.principles)

    @staticmethod
    def from_lines(lines: list[str]) -> "Principles":
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

        return Principles(principles)

    def to_dict(self):
        return self.principles

    def to_md_lines(self):
        lines = []
        lines.append("#### Principles")
        for principle in self.principles:
            lines.append(f"- {principle}")
        return lines
