from rpg.plugin import Plugin
import urllib.request
import logging
import re


class DownloadPlugin(Plugin):

    def download(self, src, dest):
        """ Tries to download file from url if it has not text MIME """
        logging.debug("DownloadPlugin: trying to download: %s, %s"
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
                        "DownloadPlugin: Content-Type: %s but Expected archive"
                        % (rurl.headers['Content-Type']))
            return False
        except Exception as ex:
            logging.error("DownloadPlugin: Failed to download '%s'\n%s"
                          % (src, str(ex)))
            return False
