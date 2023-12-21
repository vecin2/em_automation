template = """
#######################################################################################
#        config properties
#######################################################################################
{{infos["sqltask.config.props"]}}
#######################################################################################
{% set default_env_name= defaults.get("environment.name",None)%}
environment.name={{environment_name | 
                   default(default_env_name) |
                   print(infos["sqltask.config.props"])}}
container.name=ad
machine.name=localhost

#####################################################################################
# sequence.generator
#####################################################################################
{{infos["sequence.generator"]}}
#####################################################################################
{% set default_seq_gen= defaults.get("sequence.generator",None)%}
sequence.generator={{sequence_generator | 
                     default(default_seq_gen) |
                     print(infos["sequence.generator"])}}

#####################################################################################
# project.prefix
#####################################################################################
{{infos["project.prefix"]}}
#####################################################################################
{% set default_project_prefix= defaults.get("project.prefix",None)%}
project.prefix={{ project_prefix | 
                     default(default_project_prefix) |
                     print(infos["project.prefix"])}}
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
sqltask_config_props = """
# environment.name determines which config file is used, e.g:
#  work/config/show-config-txt/localdev-localhost-ad.txt """.lstrip()

sequence_generator = """
# It determines how update.sequence is computed.
# Two possible values: svn or timestamp
# - svn: uses the revision number as update.sequence
# - timestamp: uses the timestamp, equivalent to run 'date +%s' on linux""".lstrip()

project_prefix_info = """
# Used by sqltask library to set context value '_prjprefix' which is useful to compute process paths or entities relative ids
# This is two or three letters which precede project modules or project entities,
# For example when EJCustomer""".lstrip()
infos = {
    "sqltask.config.props": sqltask_config_props,
    "sequence.generator": sequence_generator,
    "project.prefix": project_prefix_info,
}
defaults = {
    "environment.name": "localdev",
    "sequence.generator": "timestamp",
    "project.prefix": "",  # need to be set so it doesn't error and works when file exists
}


def path(project_paths):
    return project_paths["core_config"]

