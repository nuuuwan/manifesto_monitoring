import re
from functools import cached_property


class NPPManifestoContents:

    @staticmethod
    def parse_l1(line):
        pattern = r"^(?:(\d+)\s+)?(\d+)\.\s+(.*)$"
        match = re.match(pattern, line)
        if not match:
            return None

        return dict(
            l1_num=int(match.group(2)),
            title=match.group(3),
        )

    @staticmethod
    def parse_l2(line):
        pattern = r'^\s*(\d+)\.(\d+)\.?\s+(.*?)\s+(\d+)\s*$'
        match = re.match(pattern, line)
        if not match:
            return None
        return dict(
            l1_num=int(match.group(1)),
            l2_num=int(match.group(2)),
            title=match.group(3),
            page_num=int(match.group(4)),
        )

    @cached_property
    def contents_lines(self):
        contents_lines = self.lines[14:59]

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
    def l1_list(self):

        l1_list = []

        for line in self.contents_lines:
            l1 = self.parse_l1(line)
            if l1:
                l1_list.append(l1)

        return l1_list

    @cached_property
    def l2_list(self):

        l2_list = []

        for line in self.contents_lines:

            l1 = self.parse_l1(line)
            if l1:
                continue

            l2 = self.parse_l2(line)
            if l2:
                l2_list.append(l2)
                continue

            if line:
                l2_list[-1]['title'] += " " + line.strip()

        return l2_list

    @cached_property
    def manifesto(self):
        l1_idx = {l1['l1_num']: l1 for l1 in self.l1_list}

        manifesto = {}
        for l2 in self.l2_list:
            l1_num = l2['l1_num']
            l1 = l1_idx[l1_num]
            l1_key = f'{l1["l1_num"]:01d}) {l1["title"]}'
            if l1_key not in manifesto:
                manifesto[l1_key] = {}

            l2_key = f'{l2["l1_num"]:01d}.{l2["l2_num"]:02d}) {l2["title"]}'
            if l2_key not in manifesto[l1_key]:
                manifesto[l1_key][l2_key] = {}

        return manifesto
