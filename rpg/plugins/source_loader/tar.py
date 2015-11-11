from rpg.plugin import Plugin
from tarfile import is_tarfile
from rpg.utils import path_to_str
from rpg.command import Command


class TarPlugin(Plugin):

    def extraction(self, source, dest):
        source = path_to_str(source)
        if is_tarfile(source):
            Command("tar xf {} -C {}".format(
                    source, path_to_str(dest))).execute()
            return True
        else:
            return False
