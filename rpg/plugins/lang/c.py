from rpg.plugin import Plugin
from rpg.command import Command
from tempfile import NamedTemporaryFile
from os import unlink, path
from re import compile
from subprocess import CalledProcessError
import logging


class CPlugin(Plugin):

    EXT_CPP = [r"cc", r"cxx", r"cpp", r"c\+\+", r"ii", r"ixx",
               r"ipp", r"i\+\+", r"hh", r"hxx", r"hpp", r"h\+\+"]

    EXT_C = [r"c", r"h"]

    EXTENSIONS = EXT_CPP + EXT_C

    @classmethod
    def get_gcc_cmd_switch(cls, file_name):
        if file_name.split(".")[-1] in cls.EXT_CPP:
            return "g++ -std=c++11 -M "
        elif file_name.split(".")[-1] in cls.EXT_C:
            return "gcc -std=c11 -M "
        else:
            return None

    def patched(self, project_dir, spec, sack):

        regex = compile(r'|'.join([r'(/usr|/include).*\.' + ex
                                   for ex in self.EXTENSIONS]))
        filter_project = compile(r'.*' + str(project_dir) + r'.*')
        f = NamedTemporaryFile(delete=False, prefix="rpg_plugin_c_")
        file_name = f.name
        f.close()

        out = Command([
            "find " + str(project_dir) + " -name " +
            " -o -name ".join(
                ["'*." + ex + "'" for ex in self.EXTENSIONS]
            )
        ]).execute()
        _ret_paths = set()
        for _f in out.splitlines():
            try:
                gcc_cmd = self.get_gcc_cmd_switch(_f)
                if not gcc_cmd:
                    continue
                Command(gcc_cmd + str(_f) + " -o " + file_name).execute()
            except CalledProcessError as e:
                logging.warn(str(e.cmd) + "\n" + str(e.output))
                continue
            with open(file_name, "r") as f:
                _ret_paths.update(
                    set([s for s in f.read().split()
                         if regex.match(s) and not filter_project.match(s)]))
            unlink(file_name)
        spec.required_files.update(_ret_paths)
        spec.build_required_files.update(_ret_paths)
