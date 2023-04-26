import os
import shutil
from datetime import datetime
from pathlib import Path

import pyperclip
from jinja2 import Environment

from sql_gen.app_project import AppProject
from sql_gen.commands.create_sql_cmd.task_prefix_generator import \
    TaskPrefixGenerator
from sql_gen.commands.print_sql_cmd import PrintSQLToConsoleCommand
from sql_gen.emproject.emsvn import EMSvn
from sql_gen.sqltask_jinja.context import ContextBuilder
from sql_gen.ui.utils import prompt, prompt_suggestions, select_string_noprompt

TaskPrefixGenerator

TaskPrefixGenerator

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

    def ask_for_sqltaskname(self, default=None, existing_task_names=None):
        if existing_task_names:
            print(
                "\nExisting tasks on that folder are:\n"
                + ", ".join(existing_task_names)
            )
        else:
            print(
                "\nNo tasks exist in this folder yet. Please follow project naming convention when entering the name, e.g. 01_ExtendCustomer"
            )
        text = "\nPlease enter the task name: "
        return prompt(text, default=default)

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
        context_builder=None,
        seq_generator=None,
        clipboard=pyperclip,
        path=None,
        template_name=None,
        template_values={},
        emprj_path=None,
        templates_path=None,
    ):
        self._app_project = None
        self.emprj_path = emprj_path
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
        self.templates_path = templates_path

    def _get_seq_generator(self, config):
        if config["sequence.generator"] == "svn":
            return EMSvn(self.emprj_path)
        else:  # if "sequence.generator==timestamp"
            return TimeStampGenerator()

    @property
    def app_project(self):
        if not self._app_project:
            self._app_project = AppProject(emprj_path=self.emprj_path)
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
        return self.app_project

    def _compute_path(self):
        prj_repo_modules_path = self.emproject.paths["sql_modules"]
        options = self._get_modules(prj_repo_modules_path)

        module_name = self.displayer.ask_for_sqlmodulename(options)
        release_name = self.app_project.get_db_release_version()
        task_folder = os.path.join(
            self.app_project.emroot,
            "modules/"
            + module_name
            + "/sqlScripts/oracle/updates/"
            + release_name
            + "/",
        )
        sqltask_name = self.displayer.ask_for_sqltaskname(
            default=self._get_current_prefix_number(task_folder),
            existing_task_names=self._list_existing_task_names(task_folder),
        )
        return task_folder + sqltask_name

    def _get_current_prefix_number(self, folder):
        existing_task_names = self._list_existing_task_names(folder)
        if existing_task_names:
            last_folder = existing_task_names[-1]
            return TaskPrefixGenerator().next(last_folder)
        return ""

    def _list_existing_task_names(self, folder):
        path = Path(folder)
        result = []
        if path.exists():
            existing_task_folders = sorted(path.iterdir())
            for folder in existing_task_folders:
                result.append(folder.name)
        return result

    def _get_modules(self, key_path):
        if not key_path.exists():
            return []
        return list(key_path.iterdir()) 

    def _user_wants_to_override(self):
        return self.displayer.ask_to_override_task(self.path) != "n"

    def _create_sql(self):
        print_sql_cmd = PrintSQLToConsoleCommand(
            context_builder=self.context_builder,
            listener=self,
            templates_path=self.templates_path,
            project_root=self.emprj_path,
        )
        print_sql_cmd.run()
        return print_sql_cmd.sql_printed()

    def on_written(self, content, template):
        self.sqltask.write(content, template)

    def _compute_update_seq_no(self):
        self.displayer.computing_rev_no(self.seq_generator.name())

        app_config = AppProject(emprj_path=self.emprj_path).config
        try:
            result = self.seq_generator.generate_seq_no(app_config, self.displayer)
        except Exception:
            result = -1
        return result


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
