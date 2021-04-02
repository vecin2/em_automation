import re
from io import StringIO


class TemplateInliner(object):
    def __init__(self, template):
        self.template = template

    def _get_template_source(self, template_name):
        return self.template.environment.loader.get_source(
            self.template.environment, template_name
        )[0]

    def inline(self):
        source = self._get_template_source(self.template.name)
        segments = IncludedTemplateParser().parse_segments(source)
        result = StringIO()
        for segment in segments:
            result.write(segment.evaluate(self.template))
        return result.getvalue()


class IncludedTemplateParser(object):
    def parse_segments(self, text):
        return self.parse(text)

    def parse(self, text):
        result = []
        index = self._append_values(text, result)
        return self._append_tail(text, result, index)

    def _append_values(self, text, result):
        regex = re.compile("{%\s*include ('|\")(.*?)('|\")\s*%}")
        index = 0
        iterator = re.finditer(regex, text)
        for match in iterator:
            if index != match.start():
                result.append(PlainText(text[index : match.start()]))
            result.append(IncludeClause(match.groups()[1]))
            index = match.end()
        return index

    def _append_tail(self, text, result, index):
        if index < len(text):
            result.append(PlainText(text[index:]))
        return result


class Segment(object):
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text

    def __eq__(self, other):
        return self.text == other.text


class IncludeClause(Segment):
    def __init__(self, text):
        super().__init__(text)

    def evaluate(self, template):
        included_template = template.environment.get_template(self.text)
        return TemplateInliner(included_template).inline()


class PlainText(Segment):
    def __init__(self, text):
        super().__init__(text)

    def evaluate(self, tempalte):
        return self.text
