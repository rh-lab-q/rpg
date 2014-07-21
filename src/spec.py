class Spec(Subpackage):
    """SPEC properties holder"""
    def __init__(self):
        self.license = None
        self.url = None
        self.vendor = None
        self.packager = None
        self.subpackages = None  # list

    def write(target_file):
        pass

    def load(source_file):
        pass

class Subpackage:
    def __init__(self):
        self.files = None  #set (source_file, target_file, is_)
        self.tags = None # dict "key" -> list[vals]
                         # hold name, version, release, summary, description,
                         # group
        self.scripts = None # dict of ["prein, ..."] -> string

    def add_tag(self, key, *vals):
        pass

    def mark_doc(self, *file):
        pass

    def mark_docdir(self, dir):
        pass
