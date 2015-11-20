#!/usr/bin/env python
import argparse
import sys
import os
import wget

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

def do_extract(args, targets):
    if args.verbose:
        print "[*] Filename: %s" % args.file[0]
        print "[*] Targets selected:"
        for target in args.targets:
            print "\t[+] %s" % target

    return_targets = {}
    for key, value in targets.iteritems():
        if key in args.targets:
            return_targets[key] = value

    args.targets       = return_targets


    return args

def do_create(args, targets):
    EXTERNAL = 'external'
    if not os.path.exists(EXTERNAL):
        os.makedirs(EXTERNAL)

    savedPath = os.getcwd()
    os.chdir(EXTERNAL)

    url_init   = 'http://web.ist.utl.pt/ist172647/ramas/external/__init__.py'
    url_module = 'http://web.ist.utl.pt/ist172647/ramas/external/newtwitter.py'
    wget.download(url_init)
    wget.download(url_module)
    os.chdir(savedPath)
    print '\n'

    sys.exit(0)

def get_cli_options(targets):
    targetsList = targets.keys()
    #Argument Parsing & Program Info
    parser = argparse.ArgumentParser(
        prog = 'ramas',
        description='%(prog)s is a memory data carving program.')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s 1')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_a = subparsers.add_parser('extract', help='Extraction command')
    parser_a.add_argument('-f', '--file', nargs=1, required=True, help='Raw memory dump file.')
    parser_a.add_argument('--html', action='store_true', help='HTML output flag.')
    parser_a.add_argument('-t', '--targets', nargs='+', action=make_list(targetsList),
        default=targetsList, help='Installed targets: '+str(targetsList))
    parser_a.add_argument('-v', '--verbose', action='store_true', help='verbose')
    #parser_a.add_argument('-m', '--modules', nargs='+', action=make_list(modulesList),
    #    default=modulesList, help='Installed modules: '+str(modulesList))
    parser_a.set_defaults(func=do_extract)

    #create_mode = False
    parser_b = subparsers.add_parser('create', help='Module creation command')
    parser_b.set_defaults(func=do_create)

    args = parser.parse_args()
    return args.func(args, targets)
