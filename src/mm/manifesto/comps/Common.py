class Common:
    @staticmethod
    def is_bullet(line: str) -> bool:
        return line.startswith("■ ") or line.startswith("• ")
