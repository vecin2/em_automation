import argparse
import os
from sql_gen.command_factory import CommandFactory
class CommandLineSQLTaskApp(object):
    """"""
    def __init__(self,args_factory=CommandFactory()):
        self.args_factory = args_factory
    def run (self,env_vars=os.environ):
        self.args_factory.make(env_vars).run()
