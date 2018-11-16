import ast
class FakeDBConnectionFactory(object):
    def __init__(self,results):
        self.results=results

    def make_conn(self,*args,**kwargs):
        return  FakeDBConnection(self.results)

class FakeDBConnection(object):
    def __init__(self,results):
        self.results = results 

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

