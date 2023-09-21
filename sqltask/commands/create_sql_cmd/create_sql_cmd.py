import shutil
from pathlib import Path

import pyperclip
from jinja2 import Environment

from sqltask.commands.create_sql_cmd.path_selector import SQLPathSelector
from sqltask.commands.create_sql_cmd.update_sequence import (
    SVNRevNoGenerator, TimeStampGenerator, UpdateSequenceWriter)
from sqltask.main.main_menu_builder import CreateSQLConfig
from sqltask.ui.utils import select_string_noprompt

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
        text = f"Are you sure you want to override the task '{path}' (y/n): "
        return select_string_noprompt(text, ["y", "n"])

    def display_sqltask_created_and_path_in_clipboard(self, filepath):
        print(f"\nSQL task created under '{filepath}' and path copied to clipboard\n")

    def update_seq_no_computed(self, number):
        print("update.sequence is '" + str(number) + "'")


class CreateSQLTaskCommand(object):
    def __init__(
        self,
        path=None,
        project=None,
    ):
        self.emproject = project
        if path:
            path = Path(path)
        self.path = path
        self.displayer = CreateSQLTaskDisplayer()
        self.clipboard = pyperclip
        self.sqltask = None
        self.path_selector = SQLPathSelector(
            self.emproject.paths["sql_modules"],
            self.emproject.get_db_release_version(),
        )

    def run(self):
        if self._get_path().exists():
            if self._user_wants_to_override():
                shutil.rmtree(self.path)  # remove task folder
            else:
                return
        self.main_menu = self._build_main_menu()
        self.main_menu.run()
        self.clipboard.copy(str(self.path))
        self.displayer.display_sqltask_created_and_path_in_clipboard(self.path)

    def _get_path(self):
        if not self.path:
            self.path = self.emproject.emroot / self.path_selector.compute_path()
        return self.path

    def _user_wants_to_override(self):
        return self.displayer.ask_to_override_task(self.path) != "n"

    def _build_main_menu(self):
        self.sqltask = FileWritter(self.path)

        update_seq_writer = UpdateSequenceWriter(self._get_seq_generator())
        scripted_sql_folder = ScriptedSQLFolder(self.sqltask, update_seq_writer)
        scripted_sql_folder.set_root(self.path)
        config = CreateSQLConfig(scripted_sql_folder)
        builder = config.get_builder(self.emproject)
        return builder.build()

    def _get_seq_generator(self):
        svn_rev_no_offset = self.emproject.config.get("svn.rev.no.offset", "0")
        sequence_generator_type = self.emproject.config["sequence.generator"]
        if sequence_generator_type == "svn":
            return SVNRevNoGenerator(self.emproject.emroot, svn_rev_no_offset)
        else:  # if "sequence.generator==timestamp"
            return TimeStampGenerator()


class ScriptedSQLFolder(object):
    def __init__(self, sqltask, update_seq_writer):
        self.file_writter = sqltask
        self.update_seq_writer = update_seq_writer
        # self.runnable_sql_writer =

    def set_root(self, path):
        self.path = path

    def on_finish(self):  # ExitHandler listener
        self.update_seq_writer.write(self.path)

    def write(self, content, template=None):
        if not self.path.exists():
            self.path.mkdir(parents=True)
        self.file_writter.write(content, template)


class FileWritter(object):
    ####################### RENAME TO STYLER (becasue \n\n\n)####
    ### does groovy have same formatting probably not,since groovy tasks are unique
    def __init__(self, path=None):
        self.path = path
        self.sql = ""

    def write(self, content, template=None):
        self.get_file_writer(template).write(self.append(content), self.path)

    def get_file_writer(self, template):
        if self.get_extension(template) == ".groovy":
            return UpdateGroovyWriter()
        if self.get_extension(template) == ".sql":
            return TableDataWritter()
        raise ValueError(
            f"{self.get_extension(template)} unsupported template extension"
        )

    def get_extension(self, template):
        return Path(template.filename).suffix

    def append(self, content):
        content = content.strip()
        if self.sql:
            # separate with two lines when multiple tasks are run
            self.sql += "\n\n\n"
        self.sql += content
        return self.sql

    def _compute_filename(self, template):
        filename = Path(template.filename)
        if filename.suffix == ".sql":
            result = "tableData.sql"
        elif filename.suffix == ".groovy":
            result = "update.groovy"
        else:
            raise ValueError(f"{filename.suffix} unsupported template extension")
        return Path(result)


class TableDataWritter(object):
    def __init__(self):
        self.filename = "tableData.sql"

    def write(self, content, path):
        (path / self.filename).write_text(content)


class UpdateGroovyWriter(object):
    def __init__(self):
        self.filename = "update.groovy"

    def write(self, content, path):
        (path / self.filename).write_text(content)
        self.write_update_xml(path)

    def write_update_xml(self, parent_folder):
        sqlpath = SQLPath(parent_folder)
        rendered_update_xml = update_xml_template.render(
            upgrade_file_base=sqlpath.upgrade_file_base()
        )
        (parent_folder / "update.xml").write_text(rendered_update_xml)


class SQLPath(object):
    def __init__(self, path):
        self.path = path

    def release_name(self):
        # self.path something like:
        # <project.home>/modules/DuWebIntegration/sqlScripts/oracle/updates/DU_01/task_name
        return self.path.parent.name

    def task_name(self):
        # self.path something like:
        # <project.home>/modules/DuWebIntegration/sqlScripts/oracle/updates/DU_01/task_name
        return self.path.name

    def module_name(self):
        # self.path something like:
        # <project.home>/modules/DuWebIntegration/sqlScripts/oracle/updates/DU_01/task_name
        parts = self.path.parts
        return parts[parts.index("modules") + 1]

    def upgrade_file_base(self):
        return f"{self.module_name()}_{self.release_name()}_{self.task_name()}"
