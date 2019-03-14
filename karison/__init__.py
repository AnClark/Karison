"""
__init__.py - Mark that karison is a package
"""

import sys

"""
Version code
"""
VERSION = (0, 0, 1)

def gen_version_str():
    v = ""
    for i in VERSION:
        v += str(i)
        v += "."
    return v[:len(v) - 1]


"""
Global variables
"""
args = None



