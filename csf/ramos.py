#!/usr/bin/env python
from platforms import *
from interfaces import *
import outputs

def main():

    # ** cli_parser.ARGS **
    # * file[]
    # * html bool
    # * target[]
    args     = get_cli_options()
    filename = args.file[0]
    targets  = args.target

    file_handler = open(filename, "r")
    if args.html:
        output = outputs.htmlOutput()
    else:
        output = outputs.textOutput()

    # ** cli_parser.CHOICES **
    # * CHOICES[0] = 'twitter'
    # * CHOICES[1] = 'facebook'
    # * CHOICES[2] = 'gmail'
    # * CHOICES[3] = 'pidgin'

    if CHOICES[0] in targets:
        twitter_set      = get_twitter_set(file_handler)
        twitter_timeline = get_twitter_timeline(twitter_set)
        output.append(twitter_timeline, outputs.PLATFORM["twitter"])


if __name__ == "__main__":
    main()
