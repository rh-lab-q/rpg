from subprocess import call
from re import sub
import ctypes


def path_to_str(path):
    return sub(r"(\s)", r"\\\1", str(path))


def copy_file(location, target):
    call(["cp", path_to_str(location), path_to_str(target)])


def get_architecture():
    return 8 * ctypes.sizeof(ctypes.c_voidp)
