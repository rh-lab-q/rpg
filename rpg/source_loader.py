import errno
import logging
import os
import os.path
import re
import shutil
import sys
import tarfile as tar
import zipfile as zip


class SourceLoader:

    TAR_GZIP = 0
    TAR_BZIP2 = 1
    TAR_LZMA = 2

    _tar_compression_mode = {"\x1f\x8b\x08": "gz",
                             "\x42\x5a\x68": "bz2",
                             "\xfd\x37\x7a\x58\x5a\x00": "xz",
                             }

    _tar_compression_type = {TAR_GZIP: "\x1f\x8b\x08",
                             TAR_BZIP2: "\x42\x5a\x68",
                             TAR_LZMA: "\xfd\x37\x7a\x58\x5a\x00"}

    def _get_compression_method(self, name):
        """determine the compression method used for a tar file. For this purpose,
        a dictionary holds magic signatures of common compressed archives.
        """

        with open(name, 'rb') as f:
            header = f.read(max(len(mode) for mode in
                                self._tar_compression_mode.keys()))
        for magic, filetype in self._tar_compression_mode.items():

            # !!!
            # latin_1 encoding works fine compared to utf-8, which used
            # additional bytes, thus the startswith method was unable to match
            # the header against the dictionary keys
            # !!!
            if header.startswith(magic.encode('latin_1')):
                return filetype
        return None

    def create_archive(self, path, extracted_dir, compression=TAR_GZIP):
        name = os.path.basename(str(path)) + ".tar.gz"
        mode = self._tar_compression_mode.get(
            self._tar_compression_type.get(compression))
        with tar.open(name, 'w:' + mode) as tarfile:
            tarfile.add(str(extracted_dir), arcname=os.path.basename(str(path)))
        return name

    def load_sources(self, source_path, extracted_dir, compression=TAR_GZIP):
        """Extracts archive to extracted_dir and adds a flag for %prep section
        to create root directory if necessary. If argument is a directory,
        copy the directory to desired location."""

        logging.debug('load_sources(%s, %s) called' % (repr(source_path),
                      repr(extracted_dir)))
        path = str(source_path)
        extracted_dir = str(extracted_dir)

        # first we need to test, if target is a directory or an archive
        if (os.path.isfile(path)):
            tar_archive = tar.is_tarfile(path)
            zip_archive = zip.is_zipfile(path)

            if tar_archive:
                type = self._get_compression_method(path)
                tarfile = tar.open(path, 'r:' + type)
                members = tarfile.getmembers()

            elif zip_archive:
                zipfile = zip.ZipFile(path)
                members = zipfile.infolist()

            else:
                print("error: File is either not an archive or the archive is \
                not supported", file=sys.stderr)

            # test for root directory
            head = members.pop(0)
            if tar_archive:
                head_is_dir = head.isdir()
            elif zip_archive:
                head_is_dir = lambda zipinfo: zipinfo.filename.endswith('/')

            if head_is_dir:  # the very first element is dir, test it for root
                root = re.compile(head.name if tar_archive else head.filename)
                for m in members:
                    if not root.match(m.name if tar_archive else m.filename):
                        # archive does not have a rootdir
                        # add flag to SPEC, that in %prep a rootdir must be
                        # created
                        break

            archive = tarfile if tar_archive else zipfile
            try:
                archive.extractall(extracted_dir)  # same API for ZIP and TAR
            except OSError as e:
                print("error: Extraction of '{}' failed: {}"
                      .format(path,
                              os.strerror(e.errno)),
                      file=sys.stderr)
                return -1

        elif (os.path.isdir(path)):
            try:
                shutil.copytree(path, extracted_dir)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    try:
                        shutil.rmtree(extracted_dir)
                        shutil.copytree(path, extracted_dir)
                    except OSError as e:
                        if e.errno == errno.EPERM or e.errno == errno.EACCES:
                            print("error: failed creating directory tree at \
                            {}: {}".format(extracted_dir,
                                           os.strerror(e.errno)),
                                  file=sys.stderr)
                        return -1
                else:
                    return -1

        else:
            print("error: not an archive, nor a dir", file=sys.stderr)
            return -1
