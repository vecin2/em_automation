import re
import os


def split_uppercase(string):
    words = re.sub(r"([a-z])([A-Z])", r"\1 \2", string).split(" ")
    first_word = words[0]
    words[0] = first_word.capitalize()
    return " ".join(words)


def objectname(path):
    path = path.replace(".", os.sep)
    return os.path.basename(path).replace(os.sep, ".")


def objectdir(path):
    path = path.replace(".", os.sep)
    return os.path.dirname(path).replace(os.sep, ".")
