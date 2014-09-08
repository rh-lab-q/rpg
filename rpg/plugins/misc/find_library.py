from rpg.plugin import Plugin


class FindLibraryPlugin(Plugin):

    def installed(self, project_dir, spec, sack):
        dyn_libs = list(project_dir.glob('**/lib*.so*'))
        static_libs = list(project_dir.glob('**/lib*.a*'))
        if (dyn_libs[0].is_file() or static_libs[0].is_file()):

            # FIXME when Command is integrated with Spec
            spec.scripts["post"] = "-p /sbin/ldconfig"
            spec.scripts["postun"] = "-p /sbin/ldconfig"
