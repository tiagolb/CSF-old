# -*- coding: utf-8 -*-

import sys
import re


def main(input_file):

    # .+href=\\"\\/(\w+).+data-user-id=\\"(\d+).+src=\\(.+\.jpeg).+\\".+data-aria-label-part=\\"0\\">(.+)<\\/p>
    # DirectMessage--(sent|received).+data-message-id=\\"(\d+).+href=\\"\\/(\w+).+data-user-id=\\"(\d+).+src=\\"(.+\.jpg)data-aria-label-part=\\0\\">([^<]+)<


    # p = re.compile(r"""<div.*?DirectMessage--(sent|received).*?data-message-id="(\d+)""", re.VERBOSE | re.DOTALL)

    message_type = r"""<div.*?DirectMessage--(sent|received).*?data-message-id="(\d+)"""

    handler = r"""a\s*href="([^"]+?)".*?data-user-id="(\d+)"""

    avatar = r"""DMAvatar-image"\s*src="([^"]+?)"."""

    content = r"""class="TweetTextSize[^>]+?>([^<]+?)<"""

    p = re.compile(".*?".join([message_type, handler, avatar, content]), re.VERBOSE | re.DOTALL)

    str = '\n'.join(input_file.readlines())

    m = set(p.findall(str))
    if m:
        print m


if __name__ == '__main__':
    main(open(sys.argv[1], "r"))
