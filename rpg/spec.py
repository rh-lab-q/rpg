from rpg.command import Command


class Subpackage(dict):

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

    def __init__(self):
        tags = {
            "Name": "",
            "Version": "",
            "Release": "",
            "Summary": "",
            "Group": "",
            "License": "",
            "URL": "",
            "Source": "",
            "Patch": "",
            "BuildArch": "",
            "BuildRoot": "",
            "Obsoletes": "",
            "Conflicts": "",
            "Vendor": "",
            "Packager": "",
            "package": "",
            "BuildRequires": [],
            "Requires": [],
            "Provides": [],
            "description": "",
            "prep": Command(),
            "build": Command(),
            "pre": Command(),
            "install": Command(),
            "check": Command(),
            "post": Command(),
            "preun": Command(),
            "postun": Command(),
            "pretrans": Command(),
            "posttrans": Command(),
            "clean": Command(),
            "changelog": Command(),
            "files": []
        }
        # list of generated translation files
        self.files_translations = []

        # (Build)Required file list that will be traslated into packages
        self.build_required_files = []
        self.required_files = []

        dict.__init__(self, tags)

    def __getattr__(self, key):
        ''' Returns attribute of chosen key from dict '''
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        ''' Set's attribute to key in dict '''
        try:
            if key in self._singles:
                if not isinstance(value, str):
                    raise TypeError(value)

            if key not in self._scripts and isinstance(value, type(Command())):
                raise TypeError(value)

            if not isinstance(value, (list, str, type(Command()))):
                raise TypeError(value)

            if key == "files" and not isinstance(value, list):
                raise TypeError(value)

            if key == "description" and not isinstance(value, str):
                raise TypeError(value)

            if key != "files" and \
                    key != "description" and \
                    not isinstance(value, Command) and \
                    key in self._scripts:
                value = Command(value)

            if key in [
                "files_translations",
                "build_required_files",
                "required_files"
            ]:
                super(Subpackage, self).__setattr__(key, value)
                return

            self.__getattr__(key)  # raises AttributeError
            self.__setitem__(key, value)
        except KeyError:
            raise AttributeError(key)

    def _get_tags(self):
        block = ''
        for ordered_key in self._singles:
            for key, value in self.items():
                if value and key is ordered_key:
                    block += key + ': ' + value + '\n'
        return block

    def _get_requires(self):
        block = ''
        for ordered_key in self._appendants:
            for key, value in self.items():
                if value and key is ordered_key:
                    for part in value:
                        block += key + ':' + '\t' + part + '\n'
        return block

    def _get_scripts(self):
        block = ''
        for ordered_key in self._scripts:
            for key, value in self.items():
                if str(value) and str(key) is ordered_key:
                    if isinstance(value, Command):
                        block += '%' + str(key) + '\n' + str(value) + '\n\n'
                    elif isinstance(value, list):
                        block += '%' + str(key) + '\n' + '\n'.join(
                            [(val[1] + " " if val[1] else "") + str(val[0])
                                for val in value]) + '\n\n' if value else ""
                    else:
                        block += '%' + str(key) + '\n' + str(value) + '\n\n'
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
        print("\n%changelog", file=out)
        for changelog in self.changelogs:
            print("{}\n".format(changelog), file=out)

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
