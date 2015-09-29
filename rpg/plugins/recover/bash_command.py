from rpg.plugin import Plugin
from re import search


class BashCommandPlugin(Plugin):

    _file = ""

    def mock_recover(self, log, spec):
        for err in log:
            match = search(
                r"\s*([^:]+)\:\s*" +
                r"[cC][oO][mM][mM][aA][nN][dD]\s*[nN][oO][tT]\s*" +
                r"[fF][oO][uU][nN][dD]", err)
            if match:
                if match.group(1) == self._file or\
                        "/usr/bin/" + match.group(1) == self._file:
                    raise RuntimeError("Couldn't resolve '{}'!"
                                       .format(match.group(1)))
                else:
                    if "/" in match.group(1):
                        self._file = match.group(1)
                    else:
                        self._file = "/usr/bin/" + match.group(1)
                spec.required_files.add(self._file)
                spec.build_required_files.add(self._file)
                return True
        return False
