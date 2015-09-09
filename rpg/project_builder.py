from shutil import copytree, rmtree
import logging


class ProjectBuilder:

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

        build_command.execute_from(project_target_dir)

    def install(self, project_source_dir, project_target_dir, install_command):
        logging.debug('install(%s, %s, %s)' % (str(project_source_dir),
                                               str(project_target_dir),
                                               str(install_command)))
        install_command.rpm_variables.append(("RPM_BUILD_ROOT",
                                              project_target_dir))
        install_command.execute_from(project_source_dir)
