"""dtask.
Usage:
  dtask 
  dtask create-sql <directory>
"""
from docopt import docopt

def parse():
    arguments = docopt(__doc__, version='dtask 0.1')
    print(arguments)
    return arguments
