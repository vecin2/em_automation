from sqltask.emproject import EMSvn


class FakeSvnClient(EMSvn):
    def __init__(self, rev_no):
        self.rev_no = rev_no

    def revision_number(self):
        if type(self.rev_no).__name__ == "str":
            return self.rev_no
        raise self.rev_no


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


def test_emsvn_sets_local_url_from_env_vars():
    emsvn = EMSvn("/home/em")
    assert "/home/em" == emsvn.local_url


def test_revision_number_returns_remote_client_entry_revision():
    local_url = "/home/em"
    remote_url = "http://fake.url.com/repo"
    local_svnclient = FakeSvnClient({"url": remote_url})
    remote_svnclient = FakeSvnClient({"entry_revision": 3})
    fake_svnclient_factory = FakeSvnClientFactory()
    fake_svnclient_factory.add_local(local_url, local_svnclient)
    fake_svnclient_factory.add_remote(remote_url, remote_svnclient)

    emsvn = EMSvn("/home/em", fake_svnclient_factory)

    result = emsvn.revision_number()
    assert 3 == result
