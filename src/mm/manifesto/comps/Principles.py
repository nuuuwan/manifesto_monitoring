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

    def to_md_lines(self, l2_topic=None):
        lines = []
        lines.append("#### Principles")
        for i_principle, principle in enumerate(self.principles, start=1):
            principle = f"P{i_principle}) {principle}"
            if l2_topic:
                principle = (
                    f"{l2_topic.l1_num}.{l2_topic.l2_num:02d}.{principle}"
                )
            lines.append(f"- {principle}")
        return lines
