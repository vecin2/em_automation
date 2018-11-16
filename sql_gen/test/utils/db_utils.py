import ast

class FakeDBConnector(object):
    def __init__(self,results):
        self.results = results
    @staticmethod
    def make(self,results):
        return FakeDBConnector(results)

    def connect(self):
        return self

    def cursor(self):
        return FakeCursor(self.results)

class FakeCursor(object):
    """mimics cursor behaviour"""
    def __init__(self,results):
        self.results = results
        headers = self.results.pop(0)
        self.description =[[name] for name in headers]

    def execute(self,string):
        pass

    def __iter__(self):
        return self.results.__iter__()

    def next(self):
        return self.results.next()

