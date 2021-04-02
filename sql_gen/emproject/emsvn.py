import os
import svn.local, svn.remote

import sql_gen
from sql_gen.emproject import current_prj_path


class SvnClientFactory(object):
    def LocalClient(self, url):
        return svn.local.LocalClient(url)

    def RemoteClient(self, url):
        return svn.remote.RemoteClient(url)


class EMSvn(object):
    def __init__(self, env_vars=os.environ, svnclient_factory=None):
        self.remote_client_var = None
        self.env_vars = env_vars
        self._svnclient_factory = svnclient_factory

    def local_client(self):
        return self.svnclient_factory.LocalClient(self.local_url)

    @property
    def local_url(self):
        return current_prj_path(self.env_vars)

    @property
    def svnclient_factory(self):
        if not self._svnclient_factory:
            self._svnclient_factory = SvnClientFactory()
        return self._svnclient_factory

    def remote_client(self):
        # cache remote client
        if self.remote_client_var is None:
            self.remote_client_var = self.svnclient_factory.RemoteClient(
                self.local_client().info()["url"]
            )
        return self.remote_client_var

    def revision_number(self):
        try:
            info = self.remote_client().info()
            sql_gen.logger.debug("Remote client info is: " + str(info))
            return info["entry_revision"]
        except Exception as excinfo:
            sql_gen.logger.exception(excinfo)
            print(
                "Unable to access svn repository to compute revision number: "
                + str(excinfo)
            )
            return -1
