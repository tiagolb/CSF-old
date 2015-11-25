#!/usr/bin/env python
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
    temp_tuple   = tempfile.mkstemp(suffix=".dump", prefix=prefix)
    temp_handler = open(temp_tuple[1], "w+")

    target_parser       = value[0]
    target_output       = value[1]
    target_preprocesser = value[2]

    target_preprocesser.process(filename, temp_handler)
    temp_handler.seek(0)

    target_parser_timeline = target_parser.get_timeline(temp_handler)
    temp_handler.close()
    target_output.setup(key, targets, html, verbose)
    target_output.out(target_parser_timeline)

def __mono_processing(filename, targets, html, verbose):
    temp_tuple   = tempfile.mkstemp(suffix=".dump", prefix="ramas")
    temp_handler = open(temp_tuple[1], "w+")

    for key, value in targets.iteritems():
        target_preprocesser = value[2]
        target_preprocesser.process(filename, temp_handler)

    for key, value in targets.iteritems():
        temp_handler.seek(0)
        target_parser = value[0]
        target_output = value[1]
        target_parser_timeline = target_parser.get_timeline(temp_handler)
        target_output.setup(key, targets, html, verbose)
        target_output.out(target_parser_timeline)

    temp_handler.close()

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
    args     = interfaces.get_cli_options(installed_targets)
    filename = args.file[0]
    targets  = args.targets
    verbose  = args.verbose
    html     = args.html
    modular  = args.modular
    threaded = args.threads

    if threaded:
        #print "THREADED"
        threads = []
        for key, value in targets.iteritems():
            #__modular_processing(filename, key, value, targets, html, verbose)
            t = threading.Thread(
                    target=__modular_processing,
                    args=[filename, key, value, targets, html, verbose])
            t.start()
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
