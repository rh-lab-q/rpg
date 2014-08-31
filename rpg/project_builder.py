from subprocess import call
from shutil import rmtree
import logging
import os
import pathlib


class ProjectBuilder:

    def build(self, project_source_dir, project_target_dir, build_params):
        """Builds project in given project_target_dir then cleans this
           directory, build_params is list of command strings.
           returns list of files that should be installed or error string"""
        logging.info('Building project')
        current_dir = os.getcwd()

        call(["cp", project_source_dir, project_target_dir, "-r", "-p"])
        root_files = self._list_files_root(project_target_dir)
        if "configure.ac" in root_files:
            call(["autoconf", "-I", project_target_dir])
            call([project_target_dir + "/configure"])
            root_files = self._list_files_root(project_target_dir)
        if "CMakeLists.txt" in root_files:
            project_build_dir = project_target_dir + "/build"
            os.mkdir(project_build_dir)
            os.chdir(project_build_dir)
            call(["cmake", project_target_dir])
            root_files = self._list_files_root(project_build_dir)
        if "Makefile" in root_files:
            if call(["make"]) != 0:
                return "Unable to build project."
            install_directory = project_target_dir + "/rpg_installed"
            if call(["make", "install", "DESTDIR=" + install_directory]) != 0:
                return "Unable to install project."
            installed_files = self._list_files(install_directory)
            rmtree(project_target_dir)
            os.chdir(current_dir)
            return installed_files
        else:
            return "Makefile not available."

    def _list_files_root(self, directory):
        return [f for f in os.listdir(directory)]

    def _list_files(self, directory):
        file_list = []
        for path, subdirs, files in os.walk(directory):
            for name in files:
                file_path = str(pathlib.PurePath(path, name))
                if not "/." in file_path:
                    file_list.append(file_path)
        return file_list

    def _apply_patch(self, patch):
        return False

    def apply_patches(self, ordered_patches):
        """Applies patches to a project_source_dir
           On failure returns the first patch, that failed"""
        for patch in ordered_patches:
            if not self._apply_patch(patch):
                return patch
