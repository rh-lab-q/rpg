from rpg.plugin import Plugin
from zipfile import is_zipfile
from rpg.utils import path_to_str
from rpg.command import Command


class ZipPlugin(Plugin):

    def extraction(self, source, dest):
        source = path_to_str(source)
        if is_zipfile(source):
            Command("unzip {} -d {}".format(
                    source, path_to_str(dest))).execute()
            return True
        else:
            return False
