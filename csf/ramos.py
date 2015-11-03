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
    output = outputs.create_output_manager(html, verbose, targets)

    if "twitter" in targets:
        twitter = TwitterParser()
        twitter_timeline = twitter.get_timeline(file_handler)
        output.append(twitter_timeline, outputs.PLATFORM["twitter"])

    file_handler.seek(0)

    if "facebook" in targets:
        facebook = FacebookParser()
        facebook_timeline = facebook.get_timeline(file_handler)
        output.append(facebook_timeline, outputs.PLATFORM["facebook"])

    file_handler.close()


if __name__ == "__main__":
    main()
