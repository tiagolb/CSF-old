#!/usr/bin/env python
import argparse

TARGETS = ['twitter', 'facebook', 'gmail', 'pidgin']

def make_list(choices):
    CHOICES = choices
    class DefaultListAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if values:
                for value in values:
                    if value not in CHOICES:
                        message = ("invalid choice: {0!r} (choose from {1})"
                                   .format(value,
                                           ', '.join([repr(action)
                                                      for action in CHOICES])))

                        raise argparse.ArgumentError(self, message)
                setattr(namespace, self.dest, values)
    return DefaultListAction

def get_cli_options(modules):
    modulesList = modules.keys()
    #Argument Parsing & Program Info
    parser = argparse.ArgumentParser(
        usage='%(prog)s -f <dump file>',
        description='%(prog)s is a memory data carving program.')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s 1')
    parser.add_argument('-f', '--file', nargs=1, required=True, help='Raw memory dump file.')
    parser.add_argument('--html', action='store_true', help='HTML output flag.')
    parser.add_argument('-t', '--targets', nargs='+', action=make_list(TARGETS), default=TARGETS, help='Installed targets: '+str(TARGETS))
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose')
    parser.add_argument('-m', '--modules', nargs='+', action=make_list(modulesList), default=modulesList, help='Installed modules: '+str(modulesList))
    args = parser.parse_args()

    if args.verbose:
        print "[*] Filename: %s" % args.file[0]
        print "[*] Targets selected:"
        for target in args.targets:
            print "\t[+] %s" % target
        print "[*] Modules selected:"
        for module in args.modules:
            print "\t[+] %s" % module

    return_modules = {}
    for key, value in modules.iteritems():
        if key in args.modules:
            return_modules[key] = value

    args.modules = return_modules

    return args
