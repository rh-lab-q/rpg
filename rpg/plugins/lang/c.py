from rpg.plugin import Plugin
from rpg.command import Command
from tempfile import NamedTemporaryFile
from os import unlink, path
from re import compile


class CPlugin(Plugin):
    def patched(self, project_dir, spec, sack):
        f = NamedTemporaryFile(delete=False, prefix="rpg_plugin_c_")
        file_name = f.name
        f.close()

        out = Command(["find " + str(project_dir)
                       + " -name *.c -o -name *.h"]).execute()

        files_list = [str(s) for s in out.splitlines()]

        makedepend = "makedepend -w10000 -f" + file_name + " -I" \
                     + str(project_dir) + " " + \
                     ' '.join(files_list) + " 2>/dev/null"
        Command(makedepend).execute()

        regex = compile(r'.*\.h')
        regex2 = compile(str(project_dir) + ".*")
        unlink(file_name + ".bak")
        with open(file_name, "r") as f:
            _ret_paths = set([path.dirname(s) for s in f.read().split()
                            if regex.match(s) and not regex2.match(s)])
        unlink(file_name)

        spec.required_files = spec.required_files.union(_ret_paths)
        spec.build_required_files = spec.build_required_files.union(_ret_paths)
