#!/usr/bin/env python3
"""
__main__.py - Main entrance of Karison

Here I have a main() function as the main entrance of Karison, 
and call it in "__name__ == 'main' " assertion.
This allows you to directly use `python -m karison` to run.

"""

# Add Karison's directory to sys.path,
# or ModuleNotFoundError will raise when exec with `python -m`.
import sys
import os.path as path
sys.path.append(path.dirname(sys.argv[0]))

# Import __init__ class
from __init__ import *

# Import comparer class
from comparer import KComparer

# Import argument parser
from arguments import parser

# Import result exporter
from result import *


def main():
    # Parse arguments
    global args
    args = parser.parse_args()

    # Extract parameters
    filename_left = args.CONFIG_LEFT[0]
    filename_right = args.CONFIG_RIGHT[0]

    # Start parsing
    comparer = KComparer(filename_left, filename_right)
    comparer.load_files()
    comparer.parse_files()

    # Compare
    compare_result = comparer.start_compare()

    # Apply filter and regex
    filtered_compare_result = comparer.filter_results(
        results=compare_result,
        filter=args.filter[0],
        regex_conf_name=args.regex[0]
    )

    # Output result
    table_exporter = TableExporter(filtered_compare_result, filename_left, filename_right)
    table_exporter.print_table()

    # Print warning for duplicated items
    comparer.warn_duplicated_items()

    # At the end of program, close stderr stream to mute down BrokenPipeError info
    # This is a disadvantage of Python...
    sys.stderr.close()


if __name__ == "__main__":
    main()
