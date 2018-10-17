from sql_gen.emproject import EMSvn

class FakeSvnClientFactory(object):
    def __init__(self):
        self.localsvnclients={}
        self.remotesvnclients={}

    def LocalClient(self, url):
        return self.localsvnclients[url]

    def RemoteClient(self, url):
        return self.remotesvnclients[url]

class  FakeSvnClient(object):
    def __init__(self,dictinfo):
        self.dictinfo=dictinfo

    def info(self):
        return self.dictinfo

def test_revision_number():
    remote_url='http://fake.url.com/repo'
    local_svnclient = FakeSvnClient({'url':remote_url})
    remote_svnclient = FakeSvnClient({'entry_revision':3})

    fake_svnclient_factory = FakeSvnClientFactory()
    fake_svnclient_factory.localsvnclients={'/em/home':local_svnclient}
    fake_svnclient_factory.remotesvnclients={remote_url:remote_svnclient}
    emsvn = EMSvn(fake_svnclient_factory)

    assert 3 == emsvn.revision_number()

