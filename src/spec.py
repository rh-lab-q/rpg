class Spec(Subpackage):
    """SPEC properties holder"""
    def __init__(self):
        self.license = None
        self.url = None
        self.vendor = None
        self.packager = None
        self.subpackages = None  # list[Subpackage]
        self.changelogs = None  # list[Changelog]
        self.patches = None  # list[str:paths]

    def write(target_file):
        pass

    def load(source_file):
        pass

    class Changelog:
        def __init__(self, date, author, email, message):
            self.date = date
            self.author = author
            self.email = email
            self.message = message

class Subpackage:
    def __init__(self):
        self.files = None  #set of tuple (source_file, target_file, tag, attr)
                           # tag could be config, doc, ghost, dir
        self.tags = None # dict "key" -> list[vals]
                         # hold name, version, release, summary, description,
                         # group
        self.scripts = None # dict of ["prein, ..."] -> string
