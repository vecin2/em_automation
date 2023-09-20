import os

from sqltask.docugen.inmemory_template_renderer import InMemoryTemplateRenderer

sqltask_config_props = """
# environment.name determines which config file is used, e.g:
#  work/config/show-config-txt/localdev-localhost-ad.txt """.lstrip()

sequence_generator = """
# It determines how update.sequence is computed.
# Two possible values: svn or timestamp
# - svn: uses the revision number as update.sequence
# - timestamp: uses the timestamp, equivalent to run 'date +%s' on linux""".lstrip()

infos = {
    "sqltask.config.props": sqltask_config_props,
    "sequence.generator": sequence_generator,
}
core_properties_template = """
#######################################################################################
#        config properties
#######################################################################################
{{infos["sqltask.config.props"]}}
#######################################################################################
environment.name={{environment_name | 
                   default(defaults["environment.name"]) |
                   print(infos["sqltask.config.props"])}}
container.name=ad
machine.name=localhost

######################################################################################
# sequence.generator
#####################################################################################
{{infos["sequence.generator"]}}
#####################################################################################
sequence.generator={{sequence_generator | 
                     default(defaults["sequence.generator"]) |
                     print(infos["sequence.generator"])}}

#####################################################################################
# svn.rev.no.offset
#####################################################################################
# This property is used only if sequence.generator=svn
# It is rarely used.
# Use in an scenario where update.sequence number does not follow the
# pattern svn rev no + 1
#####################################################################################
#svn.rev.no.offset=100

######################################################################################
#        db.release.version                                                      #
######################################################################################
# This propery is used when creating sql under:
# modules/<<module>>/sqlScripts/oracle/updates/<<db_release_version>>/<<task_name>>
# It is commented because the application it automatically computes it from releases.xml file
# Uncomment this property to override computation from release.xml file
######################################################################################
#db.release.version=PC_01
"""


class InitCommand(object):
    def __init__(self, app_project):
        self.app_project = app_project
        self.core_properties_path = self.app_project.paths["core_config"]

    def run(self):
        self.init_core_properties()
        self.init_sqltask_path()

    def init_sqltask_path(self):
        sqltask_library_path_info = """
# sqltask points to library of SQL templates 
# Please enter the library's filesystem path
# This is the folder contanining "templates" and "test_templates" folders.
# For example: c:\\em\\sqltask-library""".lstrip()
        libray_path_template = """{{sqltask_library_path |
                       default(defaults["sqltask.library.path"])|
                       print(infos["sqltask.library.path"])}}"""
        library_path_file = self.app_project.emroot / ".sqltask_library"
        default_value = "c:\\em\\sqltask-library"
        if library_path_file.exists:
            keep_going = input(
                f"{library_path_file} detected.\nThis will override the current file, do you want to continue (y/n): "
            )
            if keep_going == "y":
                default_value = library_path_file.read_text().strip()

        template_renderer = InMemoryTemplateRenderer()
        context = {
            "sqltask_library_path_info": sqltask_library_path_info,
            "default_value": default_value,
        }
        filled_template = template_renderer.render(libray_path_template, context)
        library_path_file.write_text(filled_template.lstrip())
        print(f"sqltask library path written to '{self.library_path_file}'")

    def init_core_properties(self):
        defaults = self._get_defaults()
        if defaults:
            print("Please enter the following values to configure sqltask")
            context = {"defaults": defaults, "infos": infos}
            template_renderer = InMemoryTemplateRenderer()
            filled_core_props = template_renderer.render(
                core_properties_template, context
            )
            self.core_properties_path.write_text(filled_core_props.lstrip())
            # with open(self.core_properties_path, "+w") as f:
            #     f.write(filled_template.lstrip())
            print(f"Properties written to '{self.core_properties_path}'")

    def _get_defaults(self):
        if os.path.exists(self.core_properties_path):
            keep_going = input(
                f"{self.core_properties_path} detected.\nThis will override the current file, do you want to continue (y/n): "
            )
            if keep_going == "y":
                print("Loading defaults from existing file")
                return self.app_project.config
        else:
            print(f"{self.core_properties_path}")
            return {
                "environment.name": "localdev",
                "sequence.generator": "timestamp",
            }
