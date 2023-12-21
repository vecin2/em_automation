template = """
###############################
#       edit.template.cmd
###############################
# If 'edit.template.cmd' property is set the option "--edit" shows when selecting a template is available and it runs the command configured here. 
# Curly brackets its neccesary and it will be replaced by the template path at runtime.

# Current configuration
{% set __template_editor = template_editor | suggest(["vim","notepad++","none"]) | print(infos["template.editor"])%}
{% if  __template_editor == 'vim' %}
edit.template.cmd=vim -O {}
{% elif  __template_editor == 'notepad++' %}
edit.template.cmd=notepad++.exe {}
{% set __shell = shell | suggest(["Windows","WSL"]) | print(infos["shell"])%}
  {% if  __shell == 'Windows' %}
editor.path.converter=$$(wslpath -w '{}')
  {% endif %}
{% endif %}

# Alternatives configurations: 
# 1. Using a windows cmd line or power shell with notepad++
# open templates in notepad++
# edit.template.cmd=notepad++.exe {}

# 2. Using WSL with notepad++
# edit.template.cmd=notepad++.exe {}
# editor.path.converter=$$(wslpath -w '{}')

# 3. Using any terminal with vim
# edit.template.cmd=vim -O {}
""".lstrip()
template_editor = """
When a template editor is configured the flag '--edit' is available on the choose template prompt. It will use this editor to open the selected template.\nIf you are using a different editor, select 'none' and change later the config file manually
"""
shell="""
Select 'Windows' if you are planning to run sqltask mostly within windows command prompt or powershell. Select 'WSL' if you'll be running sqltask mainly from WSL
"""
infos = {
    "template.editor": template_editor,
    "shell": shell,
}
defaults = {
    "template.editor": "notepad++",
}


def path(project_paths):
    return project_paths["local_config"]
