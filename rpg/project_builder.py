from shutil import copytree, rmtree
import logging


class ProjectBuilder:

    def build(self, project_source_dir, project_target_dir, build_command):
        """Builds project in given project_target_dir then cleans this
           directory, build_params is list of command strings.
           returns list of files that should be installed or error string"""
        logging.debug('build(%s, %s, %s)' % (repr(project_source_dir),
                      repr(project_target_dir), repr(build_command)))
        project_source_dir = str(project_source_dir)

        rmtree(str(project_target_dir))
        copytree(project_source_dir, str(project_target_dir))

        build_command.execute_from(project_target_dir)

    def _apply_patch(self, patch):
        return False

    def apply_patches(self, ordered_patches):
        """Applies patches to a project_source_dir
           On failure returns the first patch, that failed"""
        for patch in ordered_patches:
            if not self._apply_patch(patch):
                return patch
