import yaml

import sql_gen
from sql_gen.database.query_runner import QueryDict
from sql_gen.database.sqlparser import RelativeIdLoader
from sql_gen.config import ConfigFile
from sql_gen.app_project import AppProject


class Keynames(object):
    def __init__(self, dbfactory):
        self.dbfactory = dbfactory
        self._id_loader = None

    def __getitem__(self, name):
        return self.list(name)

    def full_keyname(self, keyset, id):
        return self.id_loader().full_keyname_by_id(keyset, id)

    def keyname(self, keyset, id):
        return self.id_loader().keyname_by_id(keyset, id)

    def __getattr__(self, name):
        if name.startswith("FULL_"):
            name = name.replace("FULL_", "")
            prefix = "@" + name + "."
            keynames = self.list(name)
            result = [prefix + keyname for keyname in keynames]
            result.append("NULL")
            return result
        else:
            return self.list(name)

    def id_loader(self):
        if not self._id_loader:
            self._id_loader = RelativeIdLoader(self.dbfactory.addb)
        return self._id_loader

    def list(self, keyset):
        return self.id_loader().list(keyset)

    def load(self):
        return self


class ContextBuilder(object):
    def __init__(self, app=None, emprj_path=None):
        self.app = app
        self.template_API = None
        self.context_values = None
        self.context_values_filepath = None
        self.addon_values = {}
        if not self.app:
            self.app = AppProject.make(emprj_path)

    def build(self):
        result = self.build_template_API()
        result.update(self.build_context_values())
        result.update(self.addon_values)
        return result

    def build_template_API(self):
        if self.template_API is None:
            self.template_API = {
                "_keynames": Keynames(self.app),
                "_db": self.app.ad_queryrunner,
                "_rs": self.app.rs_queryrunner,
                "_database": self.app.addb,
                "_rsdatabase": self.app.rsdb,
                "_Query": QueryDict(ConfigFile(self.app.paths["ad_queries"].path)),
                "_RSQuery": QueryDict(ConfigFile(self.app.paths["rs_queries"].path)),
                "_emprj": self.app.emproject,
            }
        return self.template_API

    def get_context_values_filepath(self):
        if not self.context_values_filepath:
            self.context_values_filepath = self.app.paths["context_values"].path
        return self.context_values_filepath

    def build_context_values(self):
        if self.context_values is None:
            self.context_values = yaml_dict(self.get_context_values_filepath())
        return self.context_values


def yaml_dict(filepath):
    try:
        with open(filepath, "r") as stream:
            yaml_dict = yaml.safe_load(stream)
            return yaml_dict
    except FileNotFoundError as exc:
        sql_gen.logger.warning(
            "No context values are added, context config file '"
            + filepath
            + "' does not exist"
        )
        return {}
    except yaml.YAMLError as exc:
        sql_gen.logger.warning(
            "No context values are added, context config file '"
            + filepath
            + "' does not exist"
        )


def init(app=None, emprj_path=None):
    return ContextBuilder(app, emprj_path).build()
