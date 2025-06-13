import re
from functools import cached_property


class NPPManifestoPDFDetails:
    @staticmethod
    def __parse_l1_heading__(line):
        # HACK!
        if 'billion SW AP loan facilities' in line:
            return None
        pattern = r"^.{0,3}(\d)\.\s?(\d{1,2})\.?\s+(.*)$"
        match = re.match(pattern, line)
        if not match:
            return None
        return {
            "l1_num": int(match.group(1)),
            "l2_num": int(match.group(2)),
            "text": match.group(3).strip(),
        }

    @cached_property
    def __l2_splits__(self):
        splits = []
        for i_line, line in enumerate(self.lines[self.I_LINE_CONTENTS_END:]):
            l2 = self.__parse_l1_heading__(line)
            if l2:
                l2 |= {"i_line": self.I_LINE_CONTENTS_END + i_line}
                splits.append(l2)
        return splits

    @cached_property
    def l1_topics(self):
        l1_topics = self.l1_topics_unexpanded
        for i_split, split in enumerate(self.__l2_splits__):
            i_start = split["i_line"]
            i_end = (
                self.__l2_splits__[i_split + 1]["i_line"]
                if i_split + 1 < len(self.__l2_splits__)
                else None
            )
            split_lines = self.lines[i_start:i_end]
            l1_topic = l1_topics[split["l1_num"] - 1]
            l2_topic = l1_topic.l2_topics[split["l2_num"] - 1]
            l2_topic.expand_fields_from_lines(split_lines)
            l1_topic.l2_topics[split["l2_num"] - 1] = l2_topic
        return l1_topics
