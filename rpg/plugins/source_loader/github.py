from rpg.plugin import Plugin
import urllib.request
import logging
import re


class GithubDownloadPlugin(Plugin):

    def download(self, src, dest):
        """ If DownloadPlugin fails, this may download the right archive,
            but only if src + "/archive/master.zip" has non-text MIME """
        if "github" in str(src) and not re.match(r".*\.[^./]+$", str(src)):
            src = str(src) + "/archive/master.zip"
            logging.debug("GithubDownloadPlugin: trying to download: %s, %s"
                          % (str(src), str(dest)))
            try:
                with urllib.request.urlopen(str(src)) as rurl:
                    if not re.match(r"text\/.*", rurl.headers['Content-Type']):
                        with open(str(dest), "wb") as fdest:
                            cont = rurl.read()
                            if cont:
                                fdest.write(cont)
                                return True
                            else:
                                return False
                    else:
                        raise IOError(
                            "GithubDownloadPlugin: Content-Type: " +
                            "%s but Expected archive"
                            % (rurl.headers['Content-Type']))
                return False
            except Exception as ex:
                logging.error(
                    "GithubDownloadPlugin: Failed to download '%s'\n%s"
                    % (src, str(ex)))
                return False
