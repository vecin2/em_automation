import os

from sql_gen.database.sqlparser import SQLParser
from sql_gen.exceptions import DatabaseError
from sql_gen.ui.utils import select_string_noprompt


class SQLRunner(object):
    def __init__(self, database, run_on_db, commit_changes=True):
        self.run_on_db = run_on_db
        self.db = database
        self.modified_db = False
        self.commit_changes = commit_changes

    def write(self, content, template=None):
        result = None
        if self.run_on_db and self._is_runnable_sql(template):
            try:
                result = self._run_content_on_db(content)
                self.db.clearcache()
            except (Exception, DatabaseError) as e:
                if input("Do you want to continue (Y/N)?") == "N":
                    raise e

        if result:
            self.display_sqltable(result)
        return result

    def on_finish(self):
        if (
            self.commit_changes
            and self.modified_db  # dont prompt to user is only selects
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
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def user_confirms_run(self):
        return self.confirm_run_sql() == "y"

    def confirm_run_sql(self):
        text = "Are you sure you want to run the above SQL (y/n): "
        return select_string_noprompt(text, ["y", "n"])
