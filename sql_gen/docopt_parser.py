"""dtask.
Usage:
    dtask print-sql
    dtask create-sql [<directory>]
    dtask test-sql [-q|-v|-vv] [--tests=<group>] [--reuse-tests]
    dtask run-sql
    dtask -h | --help

Examples:
    dtask create-sql
    dtask create-sql modules/PCCoreContactHistory/sqlScripts/oracle/updates/Pacificorp_R_0_0_1/overrideViewContactHistory

Options:
    --tests=<group>  Test which will run (all,expected-sql,run-on-db) [default: all].
    --reuse-tests    It runs tests under .tmp folder without recreate them.
    -h --help        Show usage examples
"""
from docopt import docopt


def parse():
    arguments = docopt(__doc__, version='dtask 0.1')
    #print(arguments)
    return arguments
