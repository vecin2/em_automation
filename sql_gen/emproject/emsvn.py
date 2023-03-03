import svn.local
import svn.remote

import sql_gen


class SvnClientFactory(object):
    def LocalClient(self, url):
        return svn.local.LocalClient(url)

    def RemoteClient(self, url):
        return svn.remote.RemoteClient(url)


class EMSvn(object):
    def __init__(self, local_url, svnclient_factory=None):
        self.remote_client_var = None
        self.local_url = local_url
        self._svnclient_factory = svnclient_factory

    def name(self):
        return "SVN revision number"

    def local_client(self):
        return self.svnclient_factory.LocalClient(self.local_url)

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

    def generate_seq_no(self, app_config, displayer):
        try:
            rev_no = self.revision_number()
            revision_no = int(rev_no)
            rev_no_offset = app_config.get("svn.rev.no.offset", "0")
            revision_no = revision_no + 1 + int(rev_no_offset)
            displayer.update_seq_no_computed(revision_no)
        except Exception as excinfo:
            revision_no = -1
            displayer.unable_to_compute_seq_no("-1", excinfo)
        return revision_no

    def revision_number(self):
        # should through exception if not svn repo or svn is not installed
        info = self.remote_client().info()
        sql_gen.logger.debug("Remote client info is: " + str(info))
        return info["entry_revision"]
        return info["entry_revision"]
        return info["entry_revision"]
