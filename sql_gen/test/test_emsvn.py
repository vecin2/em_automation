from sql_gen.emproject import EMSvn
import pytest

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

def make_fake_factory(local_svnclient, remote_svnclient):
    fake_svnclient_factory = FakeSvnClientFactory()
    fake_svnclient_factory.localsvnclients={'/em/home':local_svnclient}
    remote_url =local_svnclient.info()['url']
    fake_svnclient_factory.remotesvnclients={remote_url:remote_svnclient}
    return fake_svnclient_factory

def test_revision_number_return_remote_client_entry_revision():
    remote_url='http://fake.url.com/repo'
    local_svnclient = FakeSvnClient({'url':remote_url})
    remote_svnclient = FakeSvnClient({'entry_revision':3})

    emsvn = EMSvn(make_fake_factory(local_svnclient,remote_svnclient))

    assert 3 == emsvn.revision_number()

def test_revision_number_returns_zero_when_svn_not_available():
    remote_url='http://fake.url.com/repo'
    local_svnclient = FakeSvnClient({'url':remote_url})
    remote_svnclient = FakeSvnClient({})

    emsvn = EMSvn(make_fake_factory(local_svnclient,remote_svnclient))

    assert -1 == emsvn.revision_number() 
