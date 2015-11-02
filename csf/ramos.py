#!/usr/bin/env python
import argparse
from platforms import *
from interfaces import *

def main():

    # ** cli_parser.ARGS **
    # * file[]
    # * html bool
    # * target[]
    args     = get_cli_options()
    filename = args.file[0]
    targets  = args.target

    # ** cli_parser.CHOICES **
    # * CHOICES[0] = 'twitter'
    # * CHOICES[1] = 'facebook'
    # * CHOICES[2] = 'gmail'
    # * CHOICES[3] = 'pidgin'

    file_handler = open(filename, "r")

    if CHOICES[0] in targets:
        twitter_set      = get_twitter_set(file_handler)
        twitter_timeline = get_twitter_timeline(twitter_set)
        print twitter_timeline


    # if CHOICES[1] in targets:
    #     facebook(open(filename, "r"))
    # if CHOICES[2] in targets:
    #     gmail(open(filename, "r"))
    # if CHOICES[3] in targets:
    #     pidgin(open(filename, "r"))

if __name__ == "__main__":
    main()
