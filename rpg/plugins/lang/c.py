from rpg.plugin import Plugin
from rpg.command import Command
from rpg.utils import path_to_str
from re import compile
from subprocess import CalledProcessError
import logging


class CPlugin(Plugin):

    EXT_CPP = [r"cc", r"cxx", r"cpp", r"c\+\+", r"ii", r"ixx",
               r"ipp", r"i\+\+", r"hh", r"hxx", r"hpp", r"h\+\+",
               r"c", r"h"]

    def patched(self, project_dir, spec, sack):
        """ Finds dependencies via makedepend - This is not garanteed to be
            all of them. Makedepend uses macro preprocessor and if it throws
            and error makedepend didn't print deps. """
        out = Command([
            "find " + path_to_str(project_dir) + " -name " +
            " -o -name ".join(
                ["'*." + ex + "'" for ex in self.EXT_CPP]
            )
        ]).execute()
        cc_makedep = ""
        cc_included_files = []
        for _f in out.splitlines():
            try:
                cc_makedep = Command("makedepend -w 1000 " + str(_f) +
                                     " -f- 2>/dev/null").execute()
            except CalledProcessError as e:
                logging.warn(str(e.cmd) + "\n" + str(e.output))
                continue
            cc_included_files += [
                s for s in cc_makedep.split()
                if (s.startswith("/usr") or s.startswith("/include"))
                and str(project_dir) not in s]
        spec.required_files.update(cc_included_files)
        spec.build_required_files.update(cc_included_files)

    MOCK_C_ERR = compile(r"fatal error\: ([^:]*\.[^:]*)\: "
                         r"No such file or directory")

    _LAST_MISSING = ""

    def mock_recover(self, log, spec):
        """ This find dependencies makedepend didn't find. """
        for err in log:
            _missing = self.MOCK_C_ERR.search(err)
            if _missing:
                _missing = _missing.group(1)
                if self._LAST_MISSING == _missing:
                    raise RuntimeError("Can't resolve missing file '{}'"
                                       .format(_missing))
                logging.debug("Adding missing file " + _missing)
                spec.required_files.update(["*" + _missing])
                spec.build_required_files.update(["*" + _missing])
                self._LAST_MISSING = _missing
                return True
        return False
