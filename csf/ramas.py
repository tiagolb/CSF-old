#!/usr/bin/env python
import platforms
import interfaces
import outputs
import shutil, os, sys
import tempfile
import subprocess

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

def main():

    # clear result directory
    if os.path.exists(outputs.AUDIT_DIR):
        shutil.rmtree(outputs.AUDIT_DIR)

    modules_are_installed = False
    installed_modules = {}
    if module_exists("external"):
        import external
        installed_modules  = external.MODULES

    original_targets = platforms.TARGETS

    installed_targets = dict(original_targets, **installed_modules)

    # ** cli_parser.ARGS **
    # * file[]
    # * html bool
    # * target[]
    args     = interfaces.get_cli_options(installed_targets)
    filename = args.file[0]
    targets  = args.targets
    verbose  = args.verbose
    html     = args.html
    pre_processing = args.preprocessing

    #file_handler = open(filename, "r")


    file_descriptor, abs_path = tempfile.mkstemp(suffix=".temp", prefix="ramas")
    print abs_path
    file_handler = os.fdopen(file_descriptor, "w+")

    cmd = pre_processing
    print cmd
    process = subprocess.Popen(cmd, stdout=file_handler, shell=True)
    process.communicate()[0]

    for key, value in targets.iteritems():
        file_handler.seek(0)
        target_parser = value[0]
        target_output = value[1]
        target_parser_timeline = target_parser.get_timeline(file_handler)
        target_output.setup(key, targets, html, verbose)
        target_output.out(target_parser_timeline)

    file_handler.close()


if __name__ == "__main__":
    main()
