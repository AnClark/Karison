import sys
import enum

"""
Error output

Reference of text appearance in terminal: http://www.cnblogs.com/276815076/archive/2011/05/11/2043367.html
"""
def err_warning(msg):
    sys.stderr.writelines("\033[36;49;1mWARNING:\033[39;49;0m  %s\n" % msg)

def err_error(msg):
    sys.stderr.writelines("\033[31;49;1mERROR:\033[39;49;0m  %s\n" % msg)
    
def err_fatal(msg):
    sys.stderr.writelines("\033[31;49;1mFATAL:\033[39;49;0m  %s\n" % msg)

def err_other_exception(e):
    if len(e.args) >= 2:
        if isinstance(e.args[0], int):
            sys.stderr.writelines("\033[30;41;1mInternal error [%d]\033[39;49;0m: %s\n" % (e.args[0], e.args[1:]))
        else:
            sys.stderr.writelines("\033[30;41;1mInternal error:\033[39;49;0m %s\n" % str(e.args))
    else:
        sys.stderr.writelines("\033[30;41;1mInternal error:\033[39;49;0m %s\n" % str(e.args))


"""
Exit values
"""
class ExitValues(enumerate):
    EXIT_OK = 0
    EXIT_ERROR = 1
    EXIT_FATAL = 2

