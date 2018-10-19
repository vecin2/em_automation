import svn.local, svn.remote
from sql_gen.emproject import emproject_home

class SvnClientFactory(object):
    def LocalClient(self, url):
        return svn.local.LocalClient(url)

    def RemoteClient(self, url):
        return svn.remote.RemoteClient(url)

class EMSvn(object):
    def __init__(self,local_url=emproject_home(),svnclient_factory=SvnClientFactory()):
        self.svnclient_factory = svnclient_factory
        self.remote_client_var=None
        self.local_url = local_url

    def local_client(self):
        return self.svnclient_factory.LocalClient(self.local_url)

    def remote_client(self):
        #cache remote client
        if self.remote_client_var is None:
            self.remote_client_var =self.svnclient_factory.RemoteClient(self.local_client().info()['url'])
        return self.remote_client_var

    def revision_number(self):
        try:
            info = self.remote_client().info()
            return info['entry_revision']
        except:
            print("Unable to access svn repository to compute revision number")
            return -1
