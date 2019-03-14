"""
result.py - Output / export results
"""

import textwrap
import sys
from comparer import Unset

# write_to_stderr: Just ought to make code clearer
write_to_stderr = lambda text: sys.stderr.write(text)


# =================================================================
# Utility Functions
# =================================================================

# ------------------- Text Processor -------------------

def fill_and_expand(text, output_width=20, wrap_width=10):
    """
    Give a text, use textwrap.fill() to wrap text in specified width,
    then spilt its output by line, 
    finally expand each line to given output_width with a space.

    Parameters:
        text - the text you want to process.
        output_width - the width of final output. If a splitted line is
                        shorter than this, I will use a space to fill to
                        it.
        wrap_width - the width passed to textwrap.fill().

    Returns:
        a list of expanded wrapped lines.

    Example:
        * Use "|" to wrap up the output
        Given text = "On the darkness highway, cool winds in my hair."
        Invoke: textwrap.fill(text, output_width=20, wrap_width=10)
        Result:
            |On the              | -> result[0]
            |darkness            | -> result[1]
            |highway,            | -> result[2]
            |cool winds          | -> result[3]
            |in my               | -> result[4]
            |hair.               | -> result[5]
    """

    result = []
    text = textwrap.fill(text, width=wrap_width)

    for i in text.split("\n"):
        while len(i) < output_width:
            i += " "
        result.append(i)

    return result


def concatenate_wrapped_text(*str_lists):
    """
    Give an array of string lists generated by fill_and_expand(),
    then concatenate them. 
    
    Each string list is a "cell" of my table row. Items among the lists
    with a same index should be output in a line so that the final output
    can be right.

    Parameters:
        str_lists - *ARGS. Receive an array of string lists generated 
                    by fill_and_expand().

    Returns:
        Concaternated string. Just print it, then you can get the right
        table row.

    Example:
        ```
        config_name = "CONFIG_AKURA_RYU_DEMO"
        left_val = "this is a demo"
        right_val = "just print me!"
        is_same = False
        print(concatenate_wrapped_text(
            fill_and_expand(config_name, output_width=30, wrap_width=30),
            fill_and_expand(left_val, output_width=15, wrap_width=10),
            fill_and_expand(right_val, output_width=15, wrap_width=10),
            fill_and_expand(str(is_same), output_width=5, wrap_width=5)
        ), end='')
        ```
        Output:
            |CONFIG_AKURA_RYU_DEMO         this is a      just print     False|
            |                              demo           me!                 |
    """

    result = ""

    # Validate input arguments
    for item in str_lists:
        if not isinstance(item, list):
            raise ValueError("Input arguments should be a string list")

    max_line_count = max([len(i) for i in str_lists])

    # Each item in str_lists is an array of splitted lines,
    # and every those line in a same index should be concatenate into a line.
    # If an item is shorter than the others, I will use spaces as placeholder.
    i = 0
    while i < max_line_count:
        for item in str_lists:
            if i < len(item):
                result += item[i]
            else:
                result += " " * len(item[0])
        result += "\n"
        i += 1

    return result


def translate_compare_result_value(val):
    if val == Unset:
        return "<not set>"
    elif not val:
        return "<not have>"
    else:
        return val


class TableExporter(object):

    def __init__(self, compare_result, filename_left="", filename_right=""):
        self.compare_result = compare_result
        self.filename_left = str(filename_left)
        self.filename_right = str(filename_right)
        pass

    def _print_table_line(self, config_name, left_val, right_val, is_same=""):
        # The most concern problem is to handle an oversize input
        print(concatenate_wrapped_text(
            fill_and_expand(config_name, output_width=60, wrap_width=60),
            fill_and_expand(left_val, output_width=15, wrap_width=15),
            fill_and_expand(right_val, output_width=15, wrap_width=15),
            fill_and_expand(str(is_same), output_width=5, wrap_width=5)
        ), end='')


    def print_table(self, end='\n'):

        # Print filenames
        write_to_stderr("Input files:\n")
        write_to_stderr(textwrap.fill("Left:", width=10))
        write_to_stderr(self.filename_left + "\n")
        write_to_stderr(textwrap.fill("Right:", width=10))
        write_to_stderr(self.filename_right + "\n")
        write_to_stderr("\n")
        
        # Supress down BrokenPipeError
        # When redirect stdout to programs which cut off output, for example `head`, 
        # a BrokenPipeError will raise.
        try:
            # Print table head
            self._print_table_line("Config Name", "Left Value", "Right Value", "Same?")
            print('=' * 100)
            
            # Print table
            for k in self.compare_result.keys():
                self._print_table_line(
                            k,
                            translate_compare_result_value(self.compare_result[k][0]),
                            translate_compare_result_value(self.compare_result[k][1]),
                            is_same=self.compare_result[k][2]
                        )
        except BrokenPipeError:
            pass

        # Print ending string specified in args
        print(end, end='')



            
