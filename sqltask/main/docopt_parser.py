from docopt import docopt

import sqltask

help_message = """
Usage:
    {appname} init
    {appname} print-sql 
    {appname} create-sql [<directory>]
    {appname} test-sql [-q|-v|-vv] [--tests=<group>] [--test-name=<test-file>][--reuse-tests]
    {appname} run-sql
    {appname} generate-libdocs
    {appname} | -h | --help

Examples:
    {appname} create-sql
    {appname} create-sql modules/PCCoreContactHistory/sqlScripts/oracle/updates/Pacificorp_R_0_0_1/overrideViewContactHistory

Options:
    --tests=<group>         Test which will run (all,expected-sql,run-on-db) [default: all].
    --test-name=<test-file> It runs only one file  (e.g --test-name=test_verb.sql)
    --reuse-tests           It runs tests under .tmp folder without recreate them.
    -h --help               Show usage examples
"""


def parse():
    arguments = docopt(
        help_message.format(appname=sqltask.appname), version=f"{sqltask.appname} {sqltask.version}"
    )
    # print(arguments)
    return arguments
