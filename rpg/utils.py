from re import sub


def path_to_str(path):
    """ Converts path to string with escaping what needs to be escaped """
    return sub(r"(\s)", r"\\\1", str(path))


def str_to_pkgname(string):
    """ Converts any string to format suitable for package name """
    return sub(r'[^0-9a-zA-Z]', '', string)
