import importlib
def load_filters(env):
    get_template_filter=getattr(importlib.import_module("filters.description"), "get_template_filter")
    env.filters['description']=get_template_filter()

