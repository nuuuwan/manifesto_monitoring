from dataclasses import dataclass


@dataclass
class L2Chapter:
    introduction_lines: list[str]
    principles: list[str]
    activities: list[str]

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
    def __extract_activities__(lines: list[str]) -> list[str]:
        print('-' * 32)
        print('ACTIVITIES')
        print('-' * 32)

        activities = []
        has_started = False
        for line in lines:
            if line.endswith("ACTIVITIES"):
                has_started = True
                continue

            if has_started:
                if line[:2] == '■ ':
                    continue
                if (
                    len(line) > 40
                    or line[0].lower() == line[0]
                    or line[-1] == '.'
                ):
                    continue
                print(line.strip())
                activities.append(line.strip())

        return activities

    @staticmethod
    def from_lines(lines: list[str]) -> "L2Chapter":
        return L2Chapter(
            introduction_lines=L2Chapter.__extract_introduction__(lines),
            principles=L2Chapter.__extract_principles__(lines),
            activities=L2Chapter.__extract_activities__(lines),
        )
