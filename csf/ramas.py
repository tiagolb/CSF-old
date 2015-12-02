#!/usr/bin/env python
'''
The MIT License (MIT)

Copyright (c) 2015 Tiago Brito

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

__author__ = "Tiago Brito, Diogo Barradas, David Duarte"
__copyright__ = "Copyright 2015, Tiago Brito"
__credits__ = ["Tiago Brito", "Diogo Barradas", "David Duarte"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Tiago Brito"
__email__ = "tiago.de.oliveira.brito@tecnico.ulisboa.pt"
__status__ = "Production"

import platforms
import interfaces
import outputs
import shutil, os, sys
import tempfile
import threading

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

def __modular_processing(filename, key, value, targets, html, verbose):
    prefix = "ramas_"+key
    
    #create a temporary file in /tmp for this target
    temp_tuple   = tempfile.mkstemp(suffix=".dump", prefix=prefix)
    temp_handler = open(temp_tuple[1], "w+") # open the file

    target_parser       = value[0] # get the module parser component
    target_output       = value[1] # get the module output component
    target_preprocesser = value[2] # get the module preprocesser component

    target_preprocesser.process(filename, temp_handler) # preprocess the file
    temp_handler.seek(0) # go back to the beginning of the file

    # parse the file (extract information)
    target_parser_timeline = target_parser.get_timeline(temp_handler)
    temp_handler.close() # close the file
    
    # setup the output component (check if html is requested, etc.)
    target_output.setup(key, targets, html, verbose)
    target_output.out(target_parser_timeline) # output to files

def __mono_processing(filename, targets, html, verbose):
    #create a temporary file in /tmp for RAMAS
    temp_tuple   = tempfile.mkstemp(suffix=".dump", prefix="ramas")
    temp_handler = open(temp_tuple[1], "w+") # open file

    # for all targets the preprocess must be done before extracting the data
    # this way all targets receive the same preprocessed (smaller) file
    for key, value in targets.iteritems():
        target_preprocesser = value[2] # get the module preprocesser component
        target_preprocesser.process(filename, temp_handler) # preprocess the file

    # for all targets extract and output
    for key, value in targets.iteritems():
        # go back to the beginning of the file before analysing it
        temp_handler.seek(0) 
        target_parser = value[0] # get the module parser component
        target_output = value[1] # get the module parser component
        # parse the file (extract information)
        target_parser_timeline = target_parser.get_timeline(temp_handler)
        # setup the output component (check if html is requested, etc.)
        target_output.setup(key, targets, html, verbose)
        target_output.out(target_parser_timeline) # output to files

    temp_handler.close() # close the temp file


def main():
    # clear result directory
    if os.path.exists(outputs.AUDIT_DIR):
        shutil.rmtree(outputs.AUDIT_DIR)

    modules_are_installed = False
    installed_modules = {}
    
    # if the external folder is present then get the modules
    if module_exists("external"):
        import external
        installed_modules  = external.MODULES

    original_targets = platforms.TARGETS

    # concatenate both the original and external modules (installed)
    installed_targets = dict(original_targets, **installed_modules)

    # ** cli_parser.ARGS **
    # get the arguments selected
    args     = interfaces.get_cli_options(installed_targets)
    filename = args.file[0] # dump file name
    targets  = args.targets # selected targets (internal + external)
    verbose  = args.verbose # verbose flag for prints
    html     = args.html    # html tag for the output
    modular  = args.modular # modular flag for tests
    threaded = args.threads # threads flag for multithreaded execution

    if threaded:
        threads = []
        # for every module (target) a thread is created ant the function __modular_processing is called
        for key, value in targets.iteritems():
            t = threading.Thread(
                    target=__modular_processing,
                    args=[filename, key, value, targets, html, verbose])
            t.start()
            # threads are appended to this list so they can be joined next
            threads.append(t)
        for thread in threads:
            thread.join()
    elif modular:
        for key, value in targets.iteritems():
            __modular_processing(filename, key, value, targets, html, verbose)
    else: #mono
        __mono_processing(filename, targets, html, verbose)


if __name__ == "__main__":
    main()
