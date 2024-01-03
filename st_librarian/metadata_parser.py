from collections import defaultdict
from io import StringIO


class JinjaCommentParser(object):
    def __init__(self):
        self.start = "{#"
        self.end = "#}"

    def parse_from_text(self, text):
        return self.parse_first_comment(text)

    def parse_top_comment(self, text):
        if not text.lstrip().startswith(self.start):
            return ""  # only parses if there is not text before comment
        start_split = text.split(self.start)
        if len(start_split) < 2:
            return ""
        end_split = start_split[1].split(self.end)
        if len(end_split) < 2:
            return ""
        return end_split[0].strip()


class IniParser(object):
    def __init__(self, text):
        self.start_title = "["
        self.end_title = "]"
        self.text = text
        self.sections = None

    def get(self, title):
        return "".join(self.parse_sections()[title])

    def parse_sections(self):
        if not self.sections:
            self.sections = self._compute_sections()
        return self.sections

    def _compute_sections(self):
        sections = defaultdict(list)
        current_header = ""
        with StringIO(self.text) as reader:
            for line in reader:
                if self.is_header(line):
                    current_header = self.get_header_title(line)
                else:
                    if current_header:
                        sections[current_header].append(line)
        return sections

    def is_header(self, line):
        return line.lstrip().startswith("[") and line.rstrip().endswith("]")

    def get_header_title(self, line):
        return line.split("[")[1].split("]")[0]

    def get_section(self, line):
        if self.is_header(line):
            return line.split("[")[1].split("]")[0]
