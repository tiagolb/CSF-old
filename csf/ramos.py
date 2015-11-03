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
    verbose  = args.verbose
    html     = args.html

    file_handler = open(filename, "r")
    output = outputs.create_output_manager(html, verbose)

    if "twitter" in targets:
        twitter = TwitterParser()
        twitter_timeline = twitter.get_timeline(file_handler)
        output.append(twitter_timeline, outputs.PLATFORM["twitter"])


if __name__ == "__main__":
    main()
