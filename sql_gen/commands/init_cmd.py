import os

from jinja2 import DictLoader

from sql_gen.docugen.env_builder import EnvBuilder
from sql_gen.docugen.template_filler import TemplateFiller
from sql_gen.sqltask_jinja import filters as filters_package
from sql_gen.sqltask_jinja import globals as globals_module

sqltask_library_path_info = """
# Filesystem path to a specific library folder.
# This is the folder contanining "templates" and "test_templates" folders.
# For example: c:\\em\\sqltask-templates\\library""".lstrip()

sqltask_config_props = """
# The following properties determine which config file is used, e.g:
#  work/config/show-config-txt/localdev-localhost-ad.txt """.lstrip()

sequence_generator = """
# It determines how update.sequence is computed.
# Two possible values: svn or timestamp
# - svn: uses the revision number as update.sequence
# - timestamp: uses the timestamp, equivalent to run 'date +%s' on linux""".lstrip()

infos = {
    "sqltask.library.path": sqltask_library_path_info,
    "sqltask.config.props": sqltask_config_props,
    "sequence.generator": sequence_generator,
}
core_properties_template = """
#######################################################################################
#        sqltask.library.path
#######################################################################################
{{infos["sqltask.library.path"]}}
#######################################################################################
sqltask.library.path={{sqltask_library_path |
                       default(defaults["sqltask.library.path"])|
                       print(infos["sqltask.library.path"])}}
                       
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
# It is commented because the application it computes from releases.xml file
# Uncomment this property to override computation from release.xml file
######################################################################################
#db.release.version=Du_01
"""


class InitCommand(object):
    def __init__(self, app_project):
        self.app_project = app_project

    def run(self):
        print("Please enter the following values to configure sqltask")
        core_properties_path = self.app_project.paths["core_config"].path
        templates = {"template": core_properties_template}
        env = (
            EnvBuilder()
            .set_loader(DictLoader(templates))
            .set_globals_module(globals_module)
            .set_filters_package(filters_package)
            .build()
        )
        template_filler = TemplateFiller()
        template_filler.set_template(env.get_template("template"))
        defaults = None
        if os.path.exists(core_properties_path):
            keep_going = input(
                f"{core_properties_path} detected.\nThis will override the current file, do you want to continue (y/n): "
            )
            if keep_going == "y":
                print("Loading defaults from existing file")
                defaults = self.app_project.config
        else:
            print(f"{core_properties_path}")
            defaults = {
                "sqltask.library.path": "",
                "environment.name": "localdev",
                "sequence.generator": "timestamp",
            }
        if defaults:
            filled_template = template_filler.fill(
                {"defaults": defaults, "infos": infos}
            )
            with open(core_properties_path, "+w") as f:
                f.write(filled_template.lstrip())
            print(f"Properties written to '{core_properties_path}'")
