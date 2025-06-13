from dataclasses import dataclass


@dataclass
class Activity:
    l1_num: int
    l2_num: int
    activity_num: int
    title: str
    activity_items: list[str]

    def to_dict(self):
        return {
            "l1_num": self.l1_num,
            "l2_num": self.l2_num,
            "activity_num": self.activity_num,
            "title": self.title,
            "activity_items": self.activity_items,
        }

    def to_dense_dict(self):
        return {self.title: self.activity_items}

    def to_md_lines(self):
        lines = [
            "##### "
            + f"{self.l1_num:01d}.{self.l2_num:02d}.A{self.activity_num:02d})"
            + f" {self.title}"
        ]
        if self.activity_items:
            for item in self.activity_items:
                lines.append(f"- {item}")
        return lines

    def __len__(self):
        return len(self.activity_items)
