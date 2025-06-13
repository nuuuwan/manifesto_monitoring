import re


class NPPManifestoDetails:
    @staticmethod
    def parse_l1_heading(line):
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

    def get_splits_by_l1(self):
        i_match = 0
        for i_line, line in enumerate(self.lines[self.I_LINE_CONTENTS_END:]):
            l2 = self.parse_l1_heading(line)
            if l2:
                i_match += 1
                print(i_line, i_match, l2)
                continue
