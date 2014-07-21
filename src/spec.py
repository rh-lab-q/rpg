class Spec(Subpackage):
    """SPEC properties holder"""
    def __init__(self):
        self.license = None
        self.url = None
        self.vendor = None
        self.packager = None
        self.subpackages = None  # list


class Subpackage:
    def __init__(self):
        self.name = None
        self.version = None
        self.release = None
        self.summary = None
        self.description = None
        self.group = None
        self.files = None  #list

    def add_files(self, *files):
        pass

    def add_tag(self, key, *vals):
        pass

    def mark_doc(self, *file):
        pass

    def mark_docdir(self, dir):
        pass
