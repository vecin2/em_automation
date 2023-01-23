import os
import shutil
from datetime import datetime
from pathlib import Path

import pyperclip
from jinja2 import Environment

from sql_gen.app_project import AppProject
from sql_gen.commands.print_sql_cmd import (PrintSQLToConsoleCommand,
                                            PrintSQLToConsoleDisplayer)
from sql_gen.emproject.emsvn import EMSvn
from sql_gen.sqltask_jinja.context import ContextBuilder
from sql_gen.sqltask_jinja.sqltask_env import EMTemplatesEnv
from sql_gen.ui.utils import prompt_suggestions, select_string_noprompt

groovy_update_xml = """
<project name="update" default="update">
  <property name="upgrade.file.base" value="{{upgrade_file_base}}"/>
  <target name="update">
    <echo message="  userid : [${database.user}]"/>
    <echo message="  driver : [${database.driver}]"/>
    <echo message="     url : [${database.url}]"/>
    <echo message="  schema : [${database.schema}]"/>
    <echo>Writing scripts to ${sql.output.dir}/${upgrade.file.base}_upgrade.sql</echo>

    <property name="output" location="${sql.output.dir}/${upgrade.file.base}_upgrade.sql"/>
    <groovydb src="update.groovy" contextClassLoader="true">
      <classpath refid="tasks.classpath"/>
    </groovydb>
    <sqlconv-fileset file="${upgrade.file.base}.sql">
      <fileset dir="${sql.output.dir}" includes="${upgrade.file.base}_upgrade.sql"/>
    </sqlconv-fileset>
    <execute-sql file="${sql.output.dir}/${upgrade.file.base}.sql" onerror="${onerror.default.action}"/>
  </target>
  <target name="drop"/>
</project>
"""
update_xml_template = Environment().from_string(groovy_update_xml)


class CreateSQLTaskDisplayer(object):
    def ask_to_override_task(self, path):
        text = "Are you sure you want to override the task '" + path + "' (y/n): "
        return select_string_noprompt(text, ["y", "n"])

    def ask_for_sqlmodulename(self, options):
        text = "\nPlease enter the sql module name: "
        return prompt_suggestions(text, options)

    def ask_for_sqltaskname(self, options):
        text = "\nPlease enter the task name (e.g. overrideCustomer): "
        return input(text)

    def display_sqltask_created_and_path_in_clipboard(self, filepath):
        print(
            "\nSQL task created under '" + filepath + "' and path copied to clipboard\n"
        )

    def unable_to_compute_seq_no(self, rev_no, excinfo):
        message = (
            "Defaulting to\
 'PROJECT $Revision: "
            + rev_no
            + " $'. \nMake sure you update it manually!!"
        )
        print("Unable to compute sequece no:")
        print(str(excinfo))
        print(message)

    def computing_rev_no(self, sequence_generator_name):
        print(f"Computing 'update.sequence' from {sequence_generator_name}")

    def update_seq_no_computed(self, number):
        print("update.sequence is '" + str(number) + "'")


class CreateSQLTaskCommand(object):
    def __init__(
        self,
        env_vars=os.environ,
        context_builder=None,
        seq_generator=None,
        clipboard=pyperclip,
        path=None,
        template_name=None,
        template_values={},
        run_once=False,
    ):
        self._app_project = None
        self.env_vars = env_vars
        self.path = path
        if context_builder is None:
            context_builder = ContextBuilder(self.app_project)
        if seq_generator is None:
            seq_generator = self._get_seq_generator(self.app_project.config)
        self.seq_generator = seq_generator
        self.context_builder = context_builder
        self.displayer = CreateSQLTaskDisplayer()
        self.clipboard = clipboard
        self.sqltask = None
        self.template_name = template_name
        self.template_values = template_values
        self.run_once = run_once

    def _get_seq_generator(self, config):
        if config["sequence.generator"] == "svn":
            return EMSvn(self.path)
        else:  # if "sequence.generator==timestamp"
            return TimeStampGenerator()

    @property
    def app_project(self):
        if not self._app_project:
            self._app_project = AppProject(env_vars=self.env_vars)
        return self._app_project

    def run(self):
        if not self.path:
            self.path = self._compute_path()
        if os.path.exists(self.path):
            if not self._user_wants_to_override():
                return
            else:
                shutil.rmtree(self.path)  # remove task folder

        self.sqltask = SQLTask(self.path)
        self._create_sql()
        self.sqltask.update_sequence_no = self._compute_update_seq_no()
        self.sqltask.write("")  # creates update.sequence
        self.clipboard.copy(self.path)
        self.displayer.display_sqltask_created_and_path_in_clipboard(self.path)

    @property
    def emproject(self):
        return self.app_project.emproject

    def _compute_path(self):
        prj_repo_modules_path = self.emproject.paths["sql_modules"].path
        options = self._get_modules(prj_repo_modules_path)

        module_name = self.displayer.ask_for_sqlmodulename(options)
        sqltask_name = self.displayer.ask_for_sqltaskname(options)
        release_name = self.app_project.get_db_release_version()
        # release_name = self.app_project.get_latest_cre_db_release_version()
        return os.path.join(
            self.app_project.emproject.root,
            "modules/"
            + module_name
            + "/sqlScripts/oracle/updates/"
            + release_name
            + "/"
            + sqltask_name,
        )

    def _get_modules(self, key_path):
        return next(os.walk(key_path))[1]

    def _user_wants_to_override(self):
        return self.displayer.ask_to_override_task(self.path) != "n"

    def _create_sql(self):
        displayer = PrintSQLToConsoleDisplayer()
        templates_path = EMTemplatesEnv().extract_templates_path(self.env_vars)
        print_sql_cmd = PrintSQLToConsoleCommand(
            context_builder=self.context_builder,
            env_vars=self.env_vars,
            listener=self,
            template_name=self.template_name,
            template_values=self.template_values,
            run_once=self.run_once,
        )
        print_sql_cmd.run()
        return print_sql_cmd.sql_printed()

    def on_written(self, content, template):
        self.sqltask.write(content, template)

    def _compute_update_seq_no(self):
        self.displayer.computing_rev_no(self.seq_generator.name())

        app_config = AppProject(env_vars=self.env_vars).config
        return self.seq_generator.generate_seq_no(app_config, self.displayer)


class TimeStampGenerator(object):
    def generate_seq_no(self, app_config, displayer):
        seq_no = int(datetime.timestamp(datetime.now()))
        displayer.update_seq_no_computed(seq_no)
        return seq_no

    def name(self):
        return "Timestamp"


class SQLTask(object):
    def __init__(self, path=None, update_sequence_no=None):
        self.path = path
        self.update_sequence_no = update_sequence_no

    def write(self, sql, template=None):
        self._write_sql(sql, template)
        if self.update_sequence_no:
            self._write_update_sequence()

    def _write_sql(self, text, template):
        self.table_data = text
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        filename = self._compute_filename(template)
        if filename:
            filepath = Path(os.path.join(self.path, filename))
            with open(filepath, "a+") as f:
                content = self.table_data.strip()
                if filepath.exists() and filepath.read_text():
                    # separate with two lines when multiple tasks are run
                    content = "\n\n\n" + content

                f.write(content)
        if template and template.filename.endswith(".groovy"):
            upgrade_file_base = (
                f"{self.module_name()}_{self.release_name()}_{self.task_name()}"
            )
            rendered_update_xml = update_xml_template.render(
                upgrade_file_base=upgrade_file_base
            )
            with open(os.path.join(self.path, "update.xml"), "w+") as f:
                f.write(rendered_update_xml)

    def release_name(self):
        # self.path something like:
        # <project.home>/modules/DuWebIntegration/sqlScripts/oracle/updates/DU_01/task_name
        return Path(self.path).parent.name

    def task_name(self):
        # self.path something like:
        # <project.home>/modules/DuWebIntegration/sqlScripts/oracle/updates/DU_01/task_name
        return Path(self.path).name

    def module_name(self):
        # self.path something like:
        # <project.home>/modules/DuWebIntegration/sqlScripts/oracle/updates/DU_01/task_name
        parts = Path(self.path).parts
        return parts[parts.index("modules") + 1]

    def _compute_filename(self, template):
        if not template:
            return ""

        filename = template.filename
        if filename.endswith("sql"):
            return "tableData.sql"
        elif filename.endswith("groovy"):
            return "update.groovy"

    def _write_update_sequence(self):
        self.update_sequence = (
            "PROJECT $Revision: " + str(self.update_sequence_no) + " $"
        )
        with open(os.path.join(self.path, "update.sequence"), "w") as f:
            f.write(self.update_sequence)
