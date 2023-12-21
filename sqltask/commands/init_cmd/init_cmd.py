from pathlib import Path

from sqltask.commands.init_cmd import core, library, local
from sqltask.config.properties_file import PropertiesFile
from sqltask.docugen.inmemory_template_renderer import InMemoryTemplateRenderer


class InitCommand(object):
    def __init__(self, app_project):
        self.app_project = app_project
        self.core_properties_path = self.app_project.paths["core_config"]

    def run(self):
        self.init_sqltask_library_path()
        self.init_properties_file(core)
        self.init_properties_file(local)

    def init_sqltask_library_path(self):
        library_path_file = self.app_project.emroot / "project/sqltask/config/.library"
        if library_path_file.exists():
            keep_going = input(
                f"{library_path_file} detected.\nThis will override the current file, do you want to continue (y/n): "
            )
            if keep_going != "y":
                return
            defaults = {"library_path_default": library_path_file.read_text().strip()}
        else:
            defaults = library.defaults

        template_renderer = InMemoryTemplateRenderer()
        context = {
            "infos": library.infos,
            "defaults": defaults,
        }
        filled_template = template_renderer.render(library.template, context)
        library_path = Path(filled_template.lstrip())
        self.write_text_to_file(
            str(library_path).replace("\\", "\\\\"), library_path_file
        )
        print(f"sqltask library path written to '{library_path_file}'")

    def init_properties_file(self, props_files):
        filepath = props_files.path(self.app_project.paths)
        defaults = self._get_defaults(props_files)
        if defaults is not None:
            print(f"Please enter the following values to configure {filepath.name} ")
            context = {"defaults": defaults, "infos": props_files.infos}
            template_renderer = InMemoryTemplateRenderer()
            filled_core_props = template_renderer.render(props_files.template, context)
            self.write_text_to_file(filled_core_props, filepath)
            print(f"Properties written to '{filepath}'")

    def write_text_to_file(self, text, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def _get_defaults(self, props_file):
        filepath = props_file.path(self.app_project.paths)
        if filepath.exists():
            keep_going = input(
                f"{filepath} detected.\nThis will override the current file, do you want to continue (y/n): "
            )
            if keep_going == "y":
                print("Loading defaults from existing file")
                return PropertiesFile(filepath)
            else:
                return None

        else:
            print(f"{filepath}")
            return props_file.defaults
