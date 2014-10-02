from subprocess import call
import ctypes


def move_file(location, target):
    call(["mv", location, target])


def get_architecture():
    return 8 * ctypes.sizeof(ctypes.c_voidp)
