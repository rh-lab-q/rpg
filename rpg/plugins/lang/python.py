from rpg.plugin import Plugin
from rpg.command import Command
from modulefinder import ModuleFinder
import logging
import rpm


class PythonPlugin(Plugin):

    def patched(self, project_dir, spec, sack):
        for item in list(project_dir.glob('**/*.py')):
            try:
                mod = ModuleFinder()
                mod.run_script(str(item))
                for _, mod in mod.modules.items():
                    if mod.__file__ and mod.__file__.startswith("/usr/lib"):
                        spec.required_files.add(mod.__file__)
            except ImportError as ie:
                logging.warn("Exception was raised by ModuleFinder:\n" +
                             str(ie) + "\nOn file: " + str(item))

    def installed(self, project_dir, spec, sack):
        python_version = ""
        for py_file in list(project_dir.glob('**/*.py')):
            if rpm.expandMacro("%{python_sitearch}") in str(py_file) or\
                    rpm.expandMacro("%{python_sitelib}") in str(py_file):
                python_version = "python2"
            elif rpm.expandMacro("%{python3_sitearch}") in str(py_file) or\
                    rpm.expandMacro("%{python3_sitelib}") in str(py_file):
                python_version = "python3"
            Command([python_version + ' ' + sw +
                     ' -c \'import compileall; compileall.compile_file("' +
                     str(py_file) + '")\'' for sw in ["-O", ""]]).execute()
        spec.files.update([("/" + str(_f.relative_to(project_dir)), None, None)
                           for _f in project_dir.glob('**/*.py*')])
