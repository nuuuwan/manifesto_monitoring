import re
from functools import cached_property

from mm.manifesto.comps import L1Topic, L2Topic


class NPPManifestoPDFContents:
    I_LINE_CONTENTS_START = 15
    I_LINE_CONTENTS_END = 63

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

    @cached_property
    def l1_topics(self):
        l1_topics = []
        for line in self.contents_lines:
            l1_topic = L1Topic.from_line(line)
            if l1_topic:
                l1_topics.append(l1_topic)

        return l1_topics

    @cached_property
    def l2_topics(self):
        l2_list = []
        for line in self.contents_lines:

            l1 = L1Topic.from_line(line)  # DESIGN-ERROR! Duplicating
            if l1:
                continue

            l2 = L2Topic.from_line(line)
            if l2:
                l2_list.append(l2)
                continue

            if line:
                l2_list[-1]['title'] += " " + line.strip()

        return l2_list
