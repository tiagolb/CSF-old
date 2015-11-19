#!/usr/bin/env python
from platforms import *
from interfaces import *
import outputs

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

def main():

    modules_are_installed = False
    installed_modules = {}
    if module_exists("external"):
        import external
        installed_modules  = external.MODULES
        modules_are_installed = True

    # ** cli_parser.ARGS **
    # * file[]
    # * html bool
    # * target[]
    args     = get_cli_options(installed_modules)
    filename = args.file[0]
    targets  = args.targets
    verbose  = args.verbose
    html     = args.html
    modules  = args.modules
    #print modules

    file_handler = open(filename, "r")
    output = outputs.create_output_manager(html, verbose, targets)

    if modules_are_installed:
        for key, value in modules.iteritems():
            modparser = value[0]
            modparser_timeline = modparser.get_timeline(file_handler)
            modoutput = value[1]
            #print 'hello'
            modoutput.append(modparser_timeline)
            file_handler.seek(0)

    if "twitter" in targets:
        twitter = TwitterParser()
        twitter_timeline = twitter.get_timeline(file_handler)
        output.append(twitter_timeline, outputs.PLATFORM["twitter"])

    file_handler.seek(0)

    if "facebook" in targets:
        facebook = FacebookParser()
        facebook_timeline = facebook.get_timeline(file_handler)

        file_handler.seek(0)
        facebook_threads = FacebookThreadsParser()
        facebook_threads_timeline = facebook_threads.get_timeline(file_handler)

        #print facebook_timeline
        #print "###############################################################"
        #print facebook_threads_timeline


        output.append([facebook_timeline, facebook_threads_timeline],
            outputs.PLATFORM["facebook"])

    file_handler.close()


if __name__ == "__main__":
    main()
