import os
from collections import defaultdict
from enum import Enum
from pathlib import Path

from st_librarian.metadata_parser import IniParser, JinjaCommentParser
from st_librarian.naming import TaskNameParser


class TemplateInfo(object):
    def __init__(self, text):
        self.text = text
        self._ini_parser = None

    def oneline_description(self):
        return self._get_ini_parser().get("oneline_description")

    def long_description(self):
        return self._get_ini_parser().get("long_description")

    def related_tasks(self):
        return self._get_ini_parser().get("related_tasks")

    def related_views(self):
        return self._get_ini_parser().get("related_views")

    def _get_ini_parser(self):
        if not self._ini_parser:
            self._ini_parser = IniParser(self.text)
        return self._ini_parser



class Template(object):
    def __init__(self, library_root, relative_path):
        self.library_root = library_root
        self.relative_path = relative_path
        self.reader = None
        self._info = None

    def info(self):
        if not self._info:
            self._info = TemplateInfo(
                JinjaCommentParser().parse_top_comment(self.content())
            )
        return self._info

    def name(self):
        return self.relative_path.stem

    def display_name(self):
        return self.relative_path.stem.title().replace("_", " ")

    def filename(self):
        return self.relative_path.name

    def location(self):
        # relative path without top folder 'templates'
        return Path(*self.relative_path.parts[1:])

    def relpath(self):
        return self.library_root.name / self.relative_path

    def abspath(self):
        return self.library_root / self.relative_path

    def content(self):
        with open(self.abspath()) as file:
            return "".join(file.readlines())
        return ""

    def reltestpath(self):
        return self._compute_testpath_from_templatepath(self.relpath())

    def test_content(self):
        with open(self.abstestpath()) as file:
            return "".join(file.readlines())
        return ""

    def has_test(self):
        return self.abstestpath().exists()

    def abstestpath(self):
        return self._compute_testpath_from_templatepath(self.abspath())

    def _compute_testpath_from_templatepath(self, template_path):
        parts = list(template_path.parts)
        parts[parts.index("templates")] = "test_templates"
        parts[-1] = "test_" + parts[-1]  # replace filename
        return Path(*parts)

    def images(self):
        images = []
        for entry in self.abspath().parent.iterdir():
            if (
                entry.is_file()
                and entry.name.startswith(self.relative_path.stem)
                and (entry.suffix.lower() == ".jpg" or entry.suffix.lower() == ".png")
            ):
                images.append(entry)
        return images

    def related_tasks(self):
        return self._get_templates_from_string(self.info().related_tasks())

    def related_views(self):
        return self._get_templates_from_string(self.info().related_views())

    def _get_templates_from_string(self, templates):
        result = []
        template_names = templates.split(",")
        for template_name in template_names:
            if template_name:
                template = self._get_template_from_relative_path(template_name)
                result.append(template)
        return result

    def _get_template_from_relative_path(self, relative_path):
        return Template(self.library_root, self.relative_path.parent / relative_path)

    def oneline_description(self):
        return self.info().oneline_description()

    def long_description(self):
        return self.info().long_description()

    def _reader(self):
        if not self.reader:
            self.reader = open(self.relative_path_to_lib(), "r")
        return self.reader

    def update_references(self, old_name, new_name):
        self._write(self.content().replace(old_name, new_name))

    def _write(self, content):
        with open(self.abspath(), "w") as f:
            f.write(content)


class ViewType(Enum):
    BY_FOLDER = 1
    BY_ENTITY = 2


class SQLTaskLib(object):
    def __init__(self, rootpath):
        self.rootpath = rootpath
        self.templates_path = rootpath / "templates"

    def sections(self, view_type=ViewType.BY_FOLDER):
        sections = defaultdict(list)
        for current_folder, dirs, files in os.walk(self.templates_path):
            for filename in sorted(files):
                absolute_filepath = Path(current_folder + "/" + filename)
                for key in self.get_section_keys(absolute_filepath, view_type):
                    self._append_template(
                        sections[key],
                        absolute_filepath,
                    )
        return sections

    def get_section_keys(self, absolute_filepath, view_type):
        if view_type == ViewType.BY_FOLDER:
            current_folder = absolute_filepath.parent
            return [self._map_folder_to_section_name(Path(current_folder).name)]
        else:
            task_name = TaskNameParser().parse(absolute_filepath.stem)
            result = [task_name.main_entity]
            if task_name.secondary_entity:
                result.append(task_name.secondary_entity)
            return result

            raise Exception("Invalid view type")

    def list_all(self):
        result = []
        for templates in self.sections().values():
            result.extend(templates)
        return result

    def load_template(self, template_location):
        if isinstance(template_location, str):
            template_location = Path(template_location)
        absolute_path = self.templates_path / template_location
        return self._create_template(absolute_path)

    def list_all_templates(self):
        all_items = self.list_all()
        return [abs_path.relative_to(self.templates_path) for abs_path in all_items]

    def _map_folder_to_section_name(self, folder_name):
        if "templates" == folder_name:
            return "scripts"
        else:
            return folder_name

    def _append_template(self, templates, filepath):
        if self.is_template_path(filepath):
            templates.append(self._create_template(filepath))

    def is_template_path(self, filepath):
        if isinstance(filepath, str):
            filepath = Path(filepath)
        return (
            filepath.suffix == ".sql"
            or filepath.suffix == ".groovy"
            or filepath.suffix == ".txt"
        )

    def _create_template(self, filepath):
        relative_path = filepath.relative_to(self.rootpath)
        return Template(self.rootpath, relative_path)

    def db_queries(self, schema_prefix):
        file_name = f"{schema_prefix}_queries.sql"
        return self.rootpath / "db" / file_name

    def context_values(self):
        return str(self.rootpath / "config" / "context_values.yaml")

    def test_context_values(self):
        return str(self.rootpath / "config" / "test_context_values.yaml")
