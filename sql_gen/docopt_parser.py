"""dtask.
Usage:
    dtask print-sql
    dtask create-sql [<directory>]
    dtask -h | --help

Examples:
    dtask create-sql
    dtask create-sql modules/PCCoreContactHistory/sqlScripts/oracle/updates/Pacificorp_R_0_0_1/overrideViewContactHistory

Options:
    -h --help     Show this screen.
"""
from docopt import docopt


def parse():
    arguments = docopt(__doc__, version='dtask 0.1')
    #print(arguments)
    return arguments
