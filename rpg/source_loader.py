import logging
from os.path import isfile
from os.path import isdir
import re
from rpg.command import Command
from pathlib import Path


class SourceLoader(object):

    def __init__(self):
        self.prep = Command()

    def extract(self, arch, extract, compr):
        """ Extracts files from archive """

        prep = Command()
        if compr[0] == "tar":
            tar_compr = ""
            if compr[1] == "xz":
                tar_compr = "J"
            elif compr[1] == "gz":
                tar_compr = "z"
            elif compr[1] == "bz2":
                tar_compr = "j"
            elif compr[1] == "lz":
                tar_compr = "--lzip "
            elif compr[1] == "xz":
                tar_compr = "z"
            elif compr[1] == "lzma":
                tar_compr = "--lzma "
            else:
                raise SystemExit("Internal error: Unknown compression \
                    method: " + compr)
            prep.append("tar " + tar_compr + "xf " +
                        arch + " -C " + extract)
        elif compr[0] == "tgz":
            prep.append("tar xzf " + arch + " -C " + extract)
        elif compr[0] == "tbz2":
            prep.append("tar xjf " + arch + " -C " + extract)
        elif compr[0] == "zip":
            prep.append("unzip " + arch + " -d " + extract)
        elif compr[0] == "rar":
            prep.append("unrar x " + arch + " " + extract)
        elif compr[0] == "7z":
            prep.append("7z x " + arch + " -o " + extract)
        else:
            raise SystemExit("Internal error: Unknown compression \
                method: " + compr[0] + "." + compr[1])
        prep.execute()
        self.prep.append(str(prep))

    def copy_dir(self, path, ex_dir):
        """ Copies directory tree and adds command to
            prep macro """

        prep = Command("cp -rf " + path + " " + ex_dir)
        prep.execute()
        self.prep.append(str(prep))

    def process(self, ext_dir):
        i = 0
        direc = ""
        for path in Path(ext_dir).iterdir():
            i += 1
            direc = str(path)
        if i < 2:
            if isdir(direc):
                Command('mv ' + direc + '/* ' + ext_dir +
                        'rmdir ' + direc)

    def load_sources(self, source_path, extraction_dir):
        """Extracts archive to extraction_dir and adds a flag for %prep section
        to create root directory if necessary. If argument is a directory,
        copy the directory to desired location. May raise IOError """

        logging.debug('load_sources({}, {}) called'
                      .format(str(source_path), str(extraction_dir)))
        path = str(source_path)
        extraction_dir = str(extraction_dir)
        if isfile(path):
            compression = self.get_compression_method(path)
            if not compression:
                raise IOError("Input source archive '{}' is incompatible!"
                              .format(path))
            self.extract(path, extraction_dir, compression)
        elif isdir(path):
            self.copy_dir(path, extraction_dir)
        else:
            raise IOError("Input source archive/directory '{}' doesn't exists!"
                          .format(path))
        self.process(extraction_dir)
        return self.prep

    @staticmethod
    def create_archive(path, output_dir):
        """ Creates archive from folder """

        name = str(path) + ".tar.gz"
        if isdir(str(output_dir)) or \
                isfile(str(output_dir)):
            Command("tar czf " + name + " " + str(output_dir)).execute()
            return name
        else:
            raise IOError("File/directory was not found!")

    @staticmethod
    def get_compression_method(name):
        """ determine the compression method used for a tar file. """

        arch_t = re.match(r".+?\.([^.]+)(?:\.([^.]+)|)$", name)
        if not arch_t.group(1) in ["", "tar", "zip",
                                   "rar", "7z", "tgz", "tbz2"] \
            and not arch_t.group(2) in ["gz", "xz", "lz",
                                        "bz2", "Z", "lzma"]:
            return None
        return (arch_t.group(1), arch_t.group(2))
