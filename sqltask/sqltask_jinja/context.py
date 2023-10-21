import yaml

import sqltask
from sqltask.config import PropertiesFile
from sqltask.database.query_runner import QueryDict
from sqltask.database.sqlparser import RelativeIdLoader
from sqltask.docugen.inmemory_template_renderer import InMemoryTemplateRenderer


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
    def __init__(self, app=None):
        self.app = app
        self.template_API = None
        self.context_values = None
        self.context_values_filepath = None
        self.addon_values = {}

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
                "_tps": self.app.tps_queryrunner,
                "_database": self.app.addb,
                "_rsdatabase": self.app.rsdb,
                "_tpsdatabase": self.app.tpsdb,
                "_Query": QueryDict(
                    PropertiesFile(self.app.library().db_queries("ad"))
                ),
                "_RSQuery": QueryDict(
                    PropertiesFile(self.app.library().db_queries("rs"))
                ),
                "_app": self.app,
                "_config": self.app.merged_config(),
            }
        return self.template_API

    def build_context_values(self):
        if self.context_values is None:
            self.context_values = self.yaml_dict(self.get_context_values_filepath())
        return self.context_values

    def get_context_values_filepath(self):
        if not self.context_values_filepath:
            self.context_values_filepath = self.app.library().context_values()
        return self.context_values_filepath


    def yaml_dict(self, filepath):
        try:
            context_values = self.render_context_values(filepath)
            if context_values:
                return yaml.safe_load(context_values)
            return {}
        except yaml.YAMLError:
            sqltask.logger.warning(
                "No context values are added, context config file '"
                + filepath
                + "' invalid yaml format"
            )

    def render_context_values(self, filepath):
        try:
            with open(filepath, "r") as stream:
                template_renderer = InMemoryTemplateRenderer()
                
                context = {"_config": self.app.merged_config()}
                rendered_text = template_renderer.render(stream.read(), context)
                return rendered_text
        except FileNotFoundError:
            sqltask.logger.warning(
                "No context values are added, context config file '"
                + filepath
                + "' does not exist"
            )
            return ""
