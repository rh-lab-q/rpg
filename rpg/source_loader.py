import logging
from os.path import isfile, isdir
from rpg.utils import path_to_str
from pathlib import Path
from rpg.command import Command
from shutil import rmtree, copytree
from tempfile import mkdtemp


class SourceLoader(object):

    # _compressions = {
    #   compr_extension: [compr_prog, extract_switch, output_set_switch,
    #    { addition_compr_ext: [compr_prog, switch] }, ...
    # }
    _compressions = {
        "tar": [
            "tar",
            "xf",
            "-C",
            {
                "gz": [
                    "gunzip",
                    "-c"
                ],
                "xz": [
                    "xz",
                    "--decompress --stdout"
                ],
                "lz": [
                    "xz",
                    "--format=lzma --decompress --stdout"
                ],
                "lzma": [
                    "xz",
                    "--format=lzma --decompress --stdout"
                ],
                "bz2": [
                    "bzip2",
                    "-dc"
                ],
                "Z": [
                    "uncompress",
                    "-c"
                ]
            }
        ],
        "zip": [
            "unzip",
            "",
            "-d"
        ],
        "rar": [
            "unrar",
            "x",
            ""
        ],
        "7z": [
            "7z",
            "x",
            "-o"
        ],
        "tgz": [
            "tar",
            "xzf",
            "-C"
        ],
        "tbz2": [
            "tar",
            "xjf",
            "-C"
        ]
    }

    _download_block_size = 1024

    def load_sources(self, source_path, extraction_dir):
        """ If source_path is a directory, path tree will be
            copied to extraction_dir. If it is archive
            May raise IOError """

        logging.debug('load_sources({}, {}) called'
                      .format(str(source_path), str(extraction_dir)))
        path = path_to_str(source_path)
        esc_extr_dir = path_to_str(extraction_dir)
        if isfile(path):
            compression = self._get_compression_method(path)
            if not compression:
                raise IOError("Input source archive '{}' is incompatible!"
                              .format(path))
            self._extract(path, esc_extr_dir, compression)
            self._process_dir(esc_extr_dir)
        elif isdir(str(source_path)):
            self._copy_dir(str(source_path), str(extraction_dir))
        else:
            raise IOError("Input source archive/directory '{}' doesn't exists!"
                          .format(path))

    @classmethod
    def _extract(cls, arch, extraction_dir, compr):
        """ Extracts files from archive
            (can be combinated like tar and gz) """

        extr_cmd = cls._compressions[compr[0]]
        _cmd = ""
        try:
            ext_cmd = extr_cmd[3][compr[1]]
            _cmd += ext_cmd[0] + " " + ext_cmd[1] + " " + arch + " | "
            arch = "-"
        except IndexError:
            pass
        Command(_cmd + extr_cmd[0] + " " + extr_cmd[1] + " " +
                arch + " " + extr_cmd[2] + " " + extraction_dir).execute()

    @classmethod
    def _get_compression_method(cls, name):
        """ determine the compression method used for a tar file. """
        for second in cls._compressions:
            try:
                for first in cls._compressions[second][3]:
                    if name.endswith(second + "." + first):
                        return second, first
            except IndexError:
                if name.endswith(second):
                    return second, None
        raise LookupError("Couldn't resolve compression method of '{}'!"
                          .format(name))

    @classmethod
    def download_git_repo(cls, url, arch_name, branch='master'):
        """ Downloads archive from github (url) """
        compr = cls._get_compression_method(str(arch_name))
        cls.download_archive(
            str(url) + "/archive/" + branch + "." + compr[0] +
            (("." + compr[1]) if compr[1] else ""),
            arch_name)

    @classmethod
    def download_archive(cls, url, arch_name):
        """ Download file from 'url' and sets file name to 'arch_name'
            Every progress change will call callback function """
        import urllib.request
        urllib.request.urlretrieve(url, str(arch_name))

    @staticmethod
    def _copy_dir(path, ex_dir):
        """ Copies directory tree """
        rmtree(ex_dir)
        copytree(path, ex_dir)

    @staticmethod
    def _process_dir(ext_dir):
        """ Pops dir from ext_dir when needed """

        direc = [str(path) for path in Path(ext_dir).iterdir()]
        if len(direc) == 1 and isdir(direc[0]):
            direc = direc[0]
            temp = mkdtemp()
            Command('mv ' + direc + '/* ' + temp +
                    ' && rm -rf ' + direc +
                    ' && mv ' + temp + '/* ' + ext_dir).execute()
            rmtree(temp)
