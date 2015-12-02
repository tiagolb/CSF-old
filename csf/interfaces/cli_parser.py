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
    # for all targets installed
    for key, value in targets.iteritems():
        # if that target was selected insert it to the list
        if key in args.targets:
            return_targets[key] = value

    args.targets = return_targets
    return args

def do_create(args, targets):
    EXTERNAL = 'external'
    
    # create external/ folder if there is not any
    if not os.path.exists(EXTERNAL):
        os.makedirs(EXTERNAL)

    # save the local path to retrun to later
    savedPath = os.getcwd()
    # change dir to external
    os.chdir(EXTERNAL)

    # download the example module from these URLs
    url_init   = 'http://web.ist.utl.pt/ist172647/ramas/external/__init__.py'
    url_module = 'http://web.ist.utl.pt/ist172647/ramas/external/newtwitter.py'
    wget.download(url_init)
    wget.download(url_module)
    
    # return to previous dir
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
    parser_a.add_argument('--modular', action='store_true', default=False,
        help='Use Modular files (for testing)')
    parser_a.add_argument('--threads', action='store_true', default=False,
        help='Use Threads')
    parser_a.set_defaults(func=do_extract)

    #create_mode = False
    parser_b = subparsers.add_parser('create', help='Module creation command')
    parser_b.set_defaults(func=do_create)

    args = parser.parse_args()
    return args.func(args, targets)
