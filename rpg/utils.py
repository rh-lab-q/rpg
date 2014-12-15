from subprocess import call
import ctypes


def copy_file(location, target):
    call(["cp", location, target])


def get_architecture():
    return 8 * ctypes.sizeof(ctypes.c_voidp)
