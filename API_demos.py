# API k demum na 21.7. Neni Pythoni syntax.

class SPEC(Subpackage):
    
class Subpackage:
    name
    Summary
    Description
    Group
    files

    add_files([file])
    add_tag(key, [val])
    mark_doc([file])
    mark_docdir(dir)

class ProjectBuilderAnalyzer:
    # vrati seznam seznamu dependenci, kde podseznam jsou adresare kde se vsude knihovna/soubor muze nachazet, pokud je jen jedna polozka podseznamu, tak tam podseznam byt nemusi
    [[dependencies]] get_dependencies_from_cmake(directory)


class MockBuild:
    # provede build pres mock se zadanou cestou k spec filu a ke zdrojovym kodum, pripadne vrati retezec errorovych hlasek
    error/None build(spec_file, tarball)
