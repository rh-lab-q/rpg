from shutil import copytree, rmtree
import logging


class ProjectBuilder:
    """ Builds project or install it into our base directory

:Example:

>>> from rpg.project_builder import ProjectBuilder
>>> proj_builder = ProjectBuilder()
>>> proj_builder.build("/tmp/rpg-5A/source/","/tmp/rpg-5A/compiled/", "make")
>>> proj_builder.install("/tmp/rpg-5A/compiled/","/tmp/rpg-5A/installed/",
                         "make install")
"""

    def build(self, project_source_dir, project_target_dir, build_command):
        """Builds project in given project_target_dir then cleans this
           directory, build_params is list of command strings.
           returns list of files that should be installed or error string"""
        logging.debug('build(%s, %s, %s)' % (str(project_source_dir),
                                             str(project_target_dir),
                                             str(build_command)))
        project_source_dir = str(project_source_dir)

        rmtree(str(project_target_dir))
        copytree(project_source_dir, str(project_target_dir))

        build_command.execute(project_target_dir)

    def install(self, project_source_dir, project_target_dir, install_command):
        """ Installs project into our "installed" directory """
        logging.debug('install(%s, %s, %s)' % (str(project_source_dir),
                                               str(project_target_dir),
                                               str(install_command)))
        install_command.rpm_variables.append(("RPM_BUILD_ROOT",
                                              project_target_dir))
        install_command.execute(project_source_dir)
