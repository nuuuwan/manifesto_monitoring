import re
from functools import cached_property

from mm.manifesto.comps import L1Topic, L2Topic


class NPPManifestoPDFContents:
    I_LINE_CONTENTS_START = 17
    I_LINE_CONTENTS_END = 67

    @cached_property
    def contents_lines(self):
        contents_lines = self.lines[
            self.I_LINE_CONTENTS_START: self.I_LINE_CONTENTS_END
        ]

        new_contents_lines = []
        for line in contents_lines:
            # HACKS! - Need more robust way to do this.
            line = line.replace("INDEX", "")
            line = line.replace("403.7.", "03.7.")

            if re.match(r"\d.", line):
                new_contents_lines.append(line)
            elif new_contents_lines:
                new_contents_lines[-1] += " " + line.strip()
            else:
                new_contents_lines.append(line)

        return new_contents_lines

    @staticmethod
    def __process_line__(line, l1_topic_idx):
        l1 = L1Topic.from_line(line)
        if l1:
            l1_num = l1.l1_num
            if l1_num in l1_topic_idx:
                raise ValueError(f"Duplicate L1 topic number found: {l1_num}")
            l1_topic_idx[l1_num] = l1
        else:
            l2 = L2Topic.from_line(line)
            if l2:
                l1_num = l2.l1_num
                if l1_num not in l1_topic_idx:
                    raise ValueError(
                        f"L2 topic found without corresponding L1 topic: {l2}"
                    )
                l1_topic_idx[l1_num].l2_topics.append(l2)

        return l1_topic_idx

    @cached_property
    def l1_topics_unexpanded(self):
        l1_topic_idx = {}
        for line in self.contents_lines:
            l1_topic_idx = self.__process_line__(line, l1_topic_idx)

        l1_topics = list(l1_topic_idx.values())
        return l1_topics
