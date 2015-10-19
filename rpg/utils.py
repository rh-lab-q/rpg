from re import sub


def path_to_str(path):
    """ Converts path to string with escaping what needs to be escaped """
    return sub(r"(\s)", r"\\\1", str(path))
