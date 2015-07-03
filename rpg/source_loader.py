import logging
from os.path import isfile
from os.path import isdir
from pathlib import Path
import re
from rpg.command import Command
from shutil import rmtree
from shutil import copytree
from tempfile import mkdtemp
import urllib


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
        path = str(source_path)
        extraction_dir = str(extraction_dir)
        if isfile(path):
            compression = self._get_compression_method(path)
            if not compression:
                raise IOError("Input source archive '{}' is incompatible!"
                              .format(path))
            self._extract(path, extraction_dir, compression)
            self._process_dir(extraction_dir)
        elif isdir(path):
            self._copy_dir(path, extraction_dir)
        else:
            raise IOError("Input source archive/directory '{}' doesn't exists!"
                          .format(path))

    @classmethod
    def _extract(cls, arch, extraction_dir, compr):
        """ Extracts files from archive
            (can be combinated like tar and gz) """

        extr_cmd = cls._compressions[compr[0]]
        _cmd = ""
        if extr_cmd[3]:
            ext_cmd = extr_cmd[3][compr[1]]
            _cmd += ext_cmd[0] + " " + ext_cmd[1] + " " + arch + " | "
            arch = "-"
        Command(_cmd + extr_cmd[0] + " " + extr_cmd[1] + " " +
                arch + " " + extr_cmd[2] + " " + extraction_dir).execute()

    @classmethod
    def _get_compression_method(cls, name):
        """ determine the compression method used for a tar file. """

        arch_t = re.match(r".+?\.([^.]+)(?:\.([^.]+)|)$", name)
        if not arch_t.group(1) in cls._compressions \
                and not arch_t.group(2) in cls._compressions[arch_t.group(1)]:
            return None
        return (arch_t.group(1), arch_t.group(2))

    @classmethod
    def download_git_repo(cls, url, arch_name,
                          callback=None, branch='master'):
        """ Downloads archive from github (url) """
        compr = cls._get_compression_method(str(arch_name))
        cls.download_archive(
            str(url) + "/archive/" + branch + "." + compr[0] +
            (("." + compr[1]) if compr[1] else ""),
            arch_name,
            callback)

    @classmethod
    def download_archive(cls, url, arch_name, retreat_counter=0):
        """ Download file from 'url' and sets file name to 'arch_name'
            Every progress change will call callback function """
        if retreat_counter == 10:
            raise RuntimeError("Can't download '{}' - 10 times retreated"
                               .format(url))
        else:
            try:
                with open(str(arch_name), 'wb') as out_handle,\
                        urllib.request.urlopen(url) as in_handle:
                    while True:
                        buff = in_handle.read(cls._download_block_size)
                        if buff:
                            break
                        out_handle.write(buff)
            except:
                cls.download_archive(url, arch_name, retreat_counter + 1)

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
