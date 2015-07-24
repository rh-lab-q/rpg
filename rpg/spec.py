from rpg.command import Command


class Subpackage(object):

    # names of 'single' keys
    _singles = [
        "Name",
        "Version",
        "Release",
        "Summary",
        "Source",
        "Group",
        "License",
        "URL",
        "Vendor",
        "Packager",
        "BuildArch",
        "BuildRoot"
    ]

    # names of scripts
    _scripts = [
        "description",
        "prep",
        "build",
        "pre",
        "install",
        "check",
        "post",
        "preun",
        "postun",
        "pretrans",
        "posttrans",
        "clean",
        "changelog",
        "files"
    ]

    # lists that could be appended
    _appendants = [
        "Requires",
        "BuildRequires",
        "Provides"
    ]

    # tags
    Name = ""
    Version = ""
    Release = ""
    Summary = ""
    Group = ""
    License = ""
    URL = ""
    Source = ""
    Patch = ""
    BuildArch = ""
    BuildRoot = ""
    Obsoletes = ""
    Conflicts = ""
    Vendor = ""
    Packager = ""
    package = ""
    description = ""
    BuildRequires = set()
    Requires = set()
    Provides = set()
    files = []
    changelog = []
    prep = Command()
    build = Command()
    pre = Command()
    install = Command()
    check = Command()
    post = Command()
    preun = Command()
    postun = Command()
    pretrans = Command()
    posttrans = Command()
    clean = Command()

    def __init__(self):
        # list of generated translation files
        self.files_translations = []

        # (Build)Required file list that will be traslated into packages
        self.build_required_files = set()
        self.required_files = set()

    def _get_tags(self):
        block = ''
        for ordered_key in self._singles:
            value = getattr(self, ordered_key)
            if value:
                block += ordered_key + ': ' + value + '\n'
        return block

    def _get_requires(self):
        block = ''
        for ordered_key in self._appendants:
            value = getattr(self, ordered_key)
            if value:
                for part in value:
                    block += ordered_key + ':' + '\t' + part + '\n'
        return block

    def _get_scripts(self):
        block = ''
        for ordered_key in self._scripts:
            value = getattr(self, str(ordered_key))
            if str(value):
                if isinstance(value, Command):
                    block += '%' + ordered_key + '\n' + str(value) + '\n\n'
                elif isinstance(value, list):
                    block += '%' + ordered_key + '\n' + '\n'.join(
                        [(val[1] + " " if val[1] else "") + str(val[0])
                            for val in value]) + '\n\n' if value else ""
                else:
                    block += '%' + ordered_key + '\n' + str(value) + '\n\n'
        return block

    def mark_doc(self, file):
        """Helper function for GUI to mark additional files as documentation.
        Function adds '%doc' attribute to a specific file or creates a new
        entry in the set of files."""

        for f in self.files:
            if f[0] == file:
                f[1].append("%doc")
                break
        else:
            self.files.append((file, ["%doc"], None))


class Spec(Subpackage):

    """SPEC properties holder"""
    subpackages = []
    changelogs = []

    def __init__(self):
        super(Spec, self).__init__()

    def __str__(self):
        return (
            self._get_tags() +
            self._get_requires() +
            self._get_scripts()
        )

    def _write_changelog(self, out):
        out.write("\n%changelog")
        for changelog in self.changelogs:
            out.write("{}\n".format(changelog))

    def load(source_file):
        pass

    def _get_tags(self):
        return super(Spec, self)._get_tags()

    def _get_requires(self):
        return super(Spec, self)._get_requires()

    def _get_scripts(self):
        return super(Spec, self)._get_scripts()

    class Changelog:
        _weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        _months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                   "Sep", "Oct", "Nov", "Dec"]

        def __init__(self, date, author, email, *message):
            self.date = date
            self.author = author
            self.email = email
            self.message = message

        def __str__(self):
            msg = ""
            if type(self.message) is tuple:
                for m in self.message:
                    msg += "- " + m + "\n"
            else:
                msg = "- " + str(self.message) + "\n"

            return "* {} {} {} {} <{}>\n{}".format(
                self._weekdays[self.date.weekday()],
                self._months[self.date.month],
                self.date.year,
                self.author,
                self.email,
                msg)
