template = """{{sqltask_library_path |
               default(defaults["library_path_default"]) | filepath() |
               print(infos["library_path_info"])}}"""
libary_path_info = """
# sqltask points to library of SQL templates
# Please enter the tasks library filesystem path where sqltask will be pointing to
# For example: C:/em/sqltask-library
# Windows path can also be entered with '/' separator - it will be converted to backslash when writing to file""".lstrip()

infos = {"library_path_info": libary_path_info}
defaults = {"library_path_default": "C:/em/sqltask-library"}

