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

def do_extract(args, modules):
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

def do_create(args, modules):
    print "WGET"

def get_cli_options(modules):
    modulesList = modules.keys()
    #Argument Parsing & Program Info
    parser = argparse.ArgumentParser(
        prog = 'ramas',
        description='%(prog)s is a memory data carving program.')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s 1')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_a = subparsers.add_parser('extract', help='Extraction command')
    parser_a.add_argument('-f', '--file', nargs=1, required=True, help='Raw memory dump file.')
    parser_a.add_argument('--html', action='store_true', help='HTML output flag.')
    parser_a.add_argument('-t', '--targets', nargs='+',
        action=make_list(TARGETS), default=TARGETS, help='Installed targets: '+str(TARGETS))
    parser_a.add_argument('-v', '--verbose', action='store_true', help='verbose')
    parser_a.add_argument('-m', '--modules', nargs='+', action=make_list(modulesList),
        default=modulesList, help='Installed modules: '+str(modulesList))
    parser_a.set_defaults(func=do_extract)

    #create_mode = False
    parser_b = subparsers.add_parser('create', help='Module creation command')
    parser_b.set_defaults(func=do_create)

    args = parser.parse_args()
    return args.func(args, modules)
