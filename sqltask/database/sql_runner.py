import os

from sqltask.database.sqlparser import SQLParser
from sqltask.exceptions import DatabaseError
from sqltask.ui.utils import select_string_noprompt


class SQLRunner(object):
    def __init__(self, context, run_on_db, commit_changes=True):
        self.run_on_db = run_on_db
        self.context = context
        self.modified_db = False
        self.commit_changes = commit_changes
        self.db = None

    def run(self, content, template):
        result = None
        if self.run_on_db and self._is_runnable_sql(template):
            try:
                self._get_db_schema(template)
                result = self._run_content_on_db(content)
                self.db.clearcache()
            except (Exception, DatabaseError) as e:
                if input("Do you want to continue (Y/N)?") == "N":
                    raise e

        if result:
            self.display_sqltable(result)
        return result

    def write(self, content, template=None):

        return self.run(content, template)

    def _get_db_schema(self, template):
        if not self.db:
            schema_name = self._top_folder(template)
            if schema_name == "tenant_properties_service":
                self.db = self._tpsdb()
            else:
                self.db = self._addb()

        return self.db

    def _top_folder(self, template):
        template_path = template.name.split(os.sep)
        if len(template_path) > 1:
            return template_path[0]
        else:
            return ""

    def _addb(self):
        return self.context["_database"]

    def _tpsdb(self):
        return self.context["_tpsdatabase"]

    def on_finish(self):
        if (
            self.commit_changes
            and self.modified_db  # dont prompt to user if only selects stmts
            and self.user_confirms_run()
        ):
            self.commit()
        else:
            self.rollback()

    def _is_runnable_sql(self, template):
        extension = os.path.splitext(template.filename)[1]
        return extension == ".sql"

    def _run_content_on_db(self, content):
        if self.modifies_db(content):
            self.db.execute(content)
            self.modified_db = True
            return None
        else:
            return self.db.fetch(content)

    def modifies_db(self, sql):
        stmts = SQLParser().parse_statements(sql)
        for stmt in stmts:
            if not stmt.startswith("SELECT"):
                return True
        return False

    def display_sqltable(self, sqltable):
        print(str(sqltable))

    def commit(self):
        self.db and self.db.commit()

    def rollback(self):
        self.db and self.db.rollback()

    def user_confirms_run(self):
        return self.confirm_run_sql() == "y"

    def confirm_run_sql(self):
        text = "Are you sure you want to run the above SQL (y/n): "
        return select_string_noprompt(text, ["y", "n"])
