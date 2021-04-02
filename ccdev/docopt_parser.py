import sql_gen

help_message = """
Usage:
    {appname} print-sql
    {appname} create-sql [<directory>] [--template=<template_name>]
    {appname} test-sql [-q|-v|-vv] [--tests=<group>] [--test-name=<test-file>][--reuse-tests]
    {appname} run-sql [--template=<template_name>]
    {appname} extend-process <src_path> <dst_path>
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
from docopt import docopt


def parse():
    arguments = docopt(
        help_message.format(appname=sql_gen.appname), version="{appname} 0.1"
    )
    # print(arguments)
    return arguments
