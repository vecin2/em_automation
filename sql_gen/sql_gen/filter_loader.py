import importlib
def load_filters(env):
    get_template_filter=getattr(importlib.import_module("sql_gen.filters.description"), "get_template_filter")
    camelcase_get_template_filter=getattr(importlib.import_module("sql_gen.filters.camelcase"), "get_template_filter")
    env.filters['description']=get_template_filter()
    env.filters['camelcase']=camelcase_get_template_filter()

