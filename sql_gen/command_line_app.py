import argparse
from sql_gen.command_factory import CommandFactory
class CommandLineSQLTaskApp(object):
    """"""
    def __init__(self,args_factory=CommandFactory()):
        self.args_factory = args_factory
    def run (self):
        self.args_factory.make().run()
