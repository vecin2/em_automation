from sql_gen.emproject import EMSvn, current_prj_path
import pytest


class FakeSvnClientFactory(object):
    def __init__(self):
        self.localsvnclients = {}
        self.remotesvnclients = {}

    def add_local(self, key, svnclient):
        self.localsvnclients[key] = svnclient

    def add_remote(self, key, svnclient):
        self.remotesvnclients[key] = svnclient

    def LocalClient(self, url):
        return self.localsvnclients[url]

    def RemoteClient(self, url):
        return self.remotesvnclients[url]


class FakeSvnClient(object):
    def __init__(self, dictinfo={}):
        self.dictinfo = dictinfo

    def info(self):
        return self.dictinfo


env_vars = {"EM_CORE_HOME": "/home/em"}


def test_emsvn_sets_local_url_from_env_vars():
    emsvn = EMSvn(env_vars)
    assert "/home/em" == emsvn.local_url


def test_revision_number_returns_remote_client_entry_revision():
    local_url = "/home/em"
    remote_url = "http://fake.url.com/repo"
    local_svnclient = FakeSvnClient({"url": remote_url})
    remote_svnclient = FakeSvnClient({"entry_revision": 3})
    fake_svnclient_factory = FakeSvnClientFactory()
    fake_svnclient_factory.add_local(local_url, local_svnclient)
    fake_svnclient_factory.add_remote(remote_url, remote_svnclient)

    emsvn = EMSvn(env_vars, fake_svnclient_factory)

    assert 3 == emsvn.revision_number()


def test_revision_number_returns_zero_when_svn_not_available():
    local_url = "/home/em"
    remote_url = "http://fake.url.com/repo"
    local_svnclient = FakeSvnClient({"url": remote_url})
    remote_svnclient = FakeSvnClient({})
    fake_svnclient_factory = FakeSvnClientFactory()
    fake_svnclient_factory.add_local(local_url, local_svnclient)
    fake_svnclient_factory.add_remote(remote_url, remote_svnclient)

    emsvn = EMSvn(env_vars, fake_svnclient_factory)

    assert -1 == emsvn.revision_number()
