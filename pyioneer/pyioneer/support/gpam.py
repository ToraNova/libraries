################################################################################
# gpam.py - inspired by cute pammy from the office, now global !
# gpam is for functions that do not belong to a class, but still wanna print
# some stuff (verbose, error or logs). gpam provides some help to do that
# warning. high chances that gpam is desirable outside, but it is actually
# intended for internal use
# 
# @Author ToraNova
# @mailto chia_jason96@live.com
# @version 1.0
# @date 13 May 2019
################################################################################

################################################################################
# dependencies importation
################################################################################
import datetime, inspect
################################################################################
# local imports (import as if the library is a sys library)
from pyioneer.constant import ansicolor, constring
from pyioneer.support import gpam
################################################################################

# Shared with Pam
def gpam_dprint(*args,**kwargs):
    '''prints the date and the filename and func name of the caller function
    mainly for debugging purposes. use with debugprint()'''
    cframe = inspect.stack()[1]
    module = inspect.getmodule(cframe[0])
    cfilename = module.__file__
    cfuncname = cframe.function
    cdetails = "{}/func({}):".format(cfilename,cfuncname)
    print(gpam_dateDetails(constring.Dateformt.norm_micros),cdetails,*args)

# Shared with Pam
def gpam_vprint(*args, **kwargs):
    '''prints the date information only. does not include caller and file and
    function name. suitable for verboses'''
    print(gpam_dateDetails(constring.Dateformt.norm_micros),*args)

# Shared with Pam
def gpam_eprint(*args, **kwargs):
    '''error printing function. this prints the text in red'''
    cframe = inspect.stack()[1]
    module = inspect.getmodule(cframe[0])
    cfilename = module.__file__
    cfuncname = cframe.function
    cdetails = "{}/func({}):".format(cfilename,cfuncname)
    print(ansicolor.Eseq.defred + gpam_dateDetails(constring.Dateformt.norm_micros),\
            cdetails, *args, ansicolor.Eseq.normtext)

# Shared with Pam
def gpam_wprint(*args, **kwargs):
    '''warning printing function. this prints the text in yellow'''
    print(ansicolor.Eseq.defyel + gpam_dateDetails(constring.Dateformt.norm_micros),\
           *args, ansicolor.Eseq.normtext)

# Shared with Pam
def gpam_rprint(*args, **kwargs):
    '''raw print function, no dates included, just print rawly'''
    print(*args)

################################################################################
# Default setups
################################################################################
gpam_error = gpam_eprint
gpam_warn = gpam_wprint
gpam_verbose = gpam_vprint
gpam_debug = gpam_dprint
gpam_raw = gpam_rprint

################################################################################
# Macros
################################################################################
def gpam_dateDetails(sformat):
    #easy datetime macro
    return datetime.datetime.now().strftime(sformat)
    
################################################################################

def enable_gpam():
    # this enables the correct gpam function to be mapped
    global gpam_verbose
    global gpam_debug
    global gpam_raw
    gpam_verbose = gpam_vprint
    gpam_debug   = gpam_dprint
    gpam_raw = gpam_rprint

def disable_gpam():
    # this disabled, gpam are now mapped to lambda nones
    # gpam_error cannot be disabled. We do not encourage hiding errors
    global gpam_verbose
    global gpam_debug
    global gpam_raw
    gpam_verbose = lambda *a: None
    gpam_debug = lambda *a: None
    gpam_raw = lambda *a: None

# Test script
if __name__ == "__main__":
    
    gpam_warn("Warning")
    gpam_error("to err is human")
    gpam_verbose("verbose is enabled by default")
    disable_gpam()
    gpam_verbose("silenced")
    gpam_debug("silenced x2")
    gpam_error("can't silence me")
    gpam_raw("raw test 1")
    enable_gpam()
    gpam_verbose("ok' we're back")
    gpam_raw("raw test 2")

