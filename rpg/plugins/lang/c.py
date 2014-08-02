class CAnalyzer(rpg.plugin):

    @before_project_build
    @files("*.c")
    def add_c_dependencies(file, SPEC):
        pass
