"""

arguments.py - Parse arguments

"""

from __init__ import *

import argparse
import textwrap

"""
A smart formatter to print proper multiline help text.
Refered to: https://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-in-the-help-text
"""
# subclass the HelpFormatter and provide a special intro for the options 
#   that should be handled "raw" (I use "R|rest of help"):


class SmartFormatter(argparse.HelpFormatter):
    def _manual_dedent(self, text):
        lines_splitted = []

        for line in text.splitlines():
            # Ignore empty lines
            if len(line) < 1:
                continue

            # Strip heading spaces
            strip = 0
            while strip < len(line)  and  line[strip] in (' ', '\t'):
                strip += 1

            # Support manual indent. Sometimes I still want indent.
            # Use "I|" to mark up the lines to be indented
            MANUAL_INDENT = ""
            if line[strip:].startswith("I|"):
                MANUAL_INDENT = "    "

            # Return processed string array. This is what the formatter wants.
            lines_splitted.append(MANUAL_INDENT + line[strip:].replace("I|", ""))

        return lines_splitted

    def _split_lines(self, text, width):
        if text.startswith("R|"):       # If the line starts with the special marker
            return self._manual_dedent(text[2:])

        # by default, use default formatter
        return argparse.HelpFormatter._split_lines(self, text, width)   


"""
Core part
"""

# ======================= Define my ArgumentParser =======================

parser = argparse.ArgumentParser(
                                prog="karison",
                                description=textwrap.dedent("""
                                    Compare two different kernel configuration (.config, defconfig) files.
                                """),
                                formatter_class=SmartFormatter
                                )

# ======================= Add argument entries =======================

# Operand: the two config files to parse
parser.add_argument('CONFIG_LEFT', type=str, nargs=1,
                    help='Config file in the left')
parser.add_argument('CONFIG_RIGHT', type=str, nargs=1,
                    help='Config file in the right')                    

# Filter: Show specified results only
#       supports: [all*, diff, same, left_unique, right_unique] 
#                   (* represents default value)
parser.add_argument('-f', '--filter', type=str, nargs=1, default=['all'],
                    choices=[
                        'all', 'diff', 'same', 'left_unique', 'right_unique'
                        ],
                    help="""R|
                    Filter comparison result. Supported values are:
                        I|- all: Show all config items (default)
                        I|- diff: Show differ configs only
                        I|- same: Show same configs only
                        I|- left_unique: Show config items only exists in the left
                        I|- right_unique: Show config items only exists in the right
                    """
                    )

# Regular expression find: Find a config item in compared results
parser.add_argument('-r', '--regex', type=str, nargs=1, default=[""],
                    help="Find a config item in compared results")

# Version info
parser.add_argument('-v', '--version', action="version", 
                    version="Karison version: " + gen_version_str())
