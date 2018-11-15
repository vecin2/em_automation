
class FakeDBConnection(object):
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs =kwargs

    def cursor(self):
        return FakeCursor()

    def commit(self):
        return 

class FakeCursor(object):
    """mimics cursor behaviour"""
    def __init__(self):
        self.last_rows_fetched=None
        self.description=None

    def execute(self,string):
        """mimics execute behaviour"""
        self.last_rows_fetched =("12","inlineCreate")
        self.description=["ID","NAME"]

    def __iter__(self):
        return self.last_rows_fetched.__iter__()

    def next(self):
        return self.last_rows_fetched.next()

class FakeDBConnectionFactory(object):
    def __init__(self):
        self.args = None
        self.kwargs =None

    def make_conn(self,*args,**kwargs):
        self.args=args
        self.kwargs =kwargs
        return FakeDBConnection(*args,**kwargs)
