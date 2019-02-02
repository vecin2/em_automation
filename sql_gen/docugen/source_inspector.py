import inspect
import pkgutil
import importlib

def extract_module_functions(globals_module):
    all_functions = inspect.getmembers(globals_module, inspect.isfunction)
    result ={}
    result.update(all_functions)
    return result

def extract_pkg_funcs_list_by_name(filters_package,func_name):
    result={}
    module_names = _extract_module_names(filters_package)
    for module_name in module_names:
        filter_module =importlib.import_module(module_name)
        #filters which are built in  jinja do not need to be added
        if hasattr(filter_module,func_name):
            get_filter_func=getattr(filter_module,func_name)
            filter_func =get_filter_func()
            result[filter_func.__name__]=filter_func

    return result

def _extract_module_names(package):
    package_path = package.__path__
    prefix = package.__name__+"."
    modules=[]
    for _, name, _ in pkgutil.iter_modules(package_path, prefix):
        modules.append(name)
    return modules
