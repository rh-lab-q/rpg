from rpg.plugin import Plugin
from rpg.command import Command
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from os import unlink, path
from re import compile


class CPlugin(Plugin):

    def patched(self, project_dir, spec, sack):
        _ret_paths = []
        f = NamedTemporaryFile(delete=False, prefix="rpg_plugin_c_")
        fname = f.name
        f.close()
        out = Popen(["find", str(project_dir), "-name", '*.c', "-o", "-name",
                    '*.h'], stdout=PIPE)
        files_list = \
            [str(s).replace('\n', '').replace('\\n', '').replace('b\'', '\'')
             for s in out.stdout.readlines()]
        makedepend = "makedepend -w10000 -f" + fname + " -I" \
                     + str(project_dir) + " " + ' '.join(files_list)
        Command(makedepend).execute()
        regex = compile(".*\.h")
        regex2 = compile(str(project_dir) + ".*")
        unlink(fname + ".bak")
        with open(fname, "r") as f:
            _ret_paths = list(set([path.dirname(s) for s in f.read().split()
                              if regex.match(s) and not regex2.match(s)]))
        unlink(fname)
        spec.Requires += _ret_paths
        spec.BuildRequires += _ret_paths
