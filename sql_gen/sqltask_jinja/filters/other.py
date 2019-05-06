import re

def split_uppercase(string):
        return re.sub(r'([a-z])([A-Z])', r'\1 \2', string)
