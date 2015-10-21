from rpg.command import Command


class Spec:
    """ SPEC properties holder

:Example:

>>> from rpg.spec import Spec
>>> spec = Spec()
>>> spec.Name = "Example"
>>> spec.Version = "0.6.11"
>>> spec.Release = "1%{?snapshot}%{?dist}"
>>> spec.License = "GPLv2"
>>> spec.Summary = "Example ..."
>>> spec.description = ("Example ...")
>>> spec.URL = "https://github.com/example_repo"
"""
    changelogs = []

    #: names of 'single' keys
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

    #: names of scripts
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

    #: lists that could be appended
    _appendants = [
        "Requires",
        "BuildRequires",
        "Provides"
    ]

    def __init__(self):
        # tags
        self.Name = ""  #: initial value: ""
        self.Version = ""  #: initial value: ""
        self.Release = ""  #: initial value: ""
        self.Summary = ""  #: initial value: ""
        self.Group = ""  #: initial value: ""
        self.License = ""  #: initial value: ""
        self.URL = ""  #: initial value: ""
        self.Source = ""  #: initial value: ""
        self.Patch = ""  #: initial value: ""
        self.BuildArch = ""  #: initial value: ""
        self.BuildRoot = ""  #: initial value: ""
        self.Obsoletes = ""  #: initial value: ""
        self.Conflicts = ""  #: initial value: ""
        self.Vendor = ""  #: initial value: ""
        self.Packager = ""  #: initial value: ""
        self.package = ""  #: initial value: ""
        self.description = ""  #: initial value: ""
        self.BuildRequires = set()  #: initial value: set()
        self.Requires = set()  #: initial value: set()
        self.Provides = set()  #: initial value: set()
        self.files = set()  #: initial value: []
        self.changelog = []  #: initial value: []
        self.prep = Command()  #: initial value: Command()
        self.build = Command()  #: initial value: Command()
        self.pre = Command()  #: initial value: Command()
        self.install = Command()  #: initial value: Command()
        self.check = Command()  #: initial value: Command()
        self.post = Command()  #: initial value: Command()
        self.preun = Command()  #: initial value: Command()
        self.postun = Command()  #: initial value: Command()
        self.pretrans = Command()  #: initial value: Command()
        self.posttrans = Command()  #: initial value: Command()
        self.clean = Command()  #: initial value: Command()

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
                elif (isinstance(value, list) or (isinstance(value, set))):
                    block += '%' + ordered_key + '\n' + '\n'.join(
                        [(val[1] + " " if val[1] else "") + str(val[0])
                            for val in value]) + '\n\n' if value else ""
                else:
                    block += '%' + ordered_key + '\n' + str(value) + '\n\n'
        return block

    def __str__(self):
        """ Returns final representation of spec file """
        return (
            self._get_tags() +
            self._get_requires() +
            self._get_scripts()
        )

    def _write_changelog(self, out):
        """ Writes changelog into spec file """
        out.write("\n%changelog")
        for changelog in self.changelogs:
            out.write("{}\n".format(changelog))

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
