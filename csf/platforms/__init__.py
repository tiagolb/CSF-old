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
__maintainer__ = "Tiago Brito"
__email__ = "tiago.de.oliveira.brito@tecnico.ulisboa.pt"
__status__ = "Production"

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'

import twitter
import facebook
import facebookThreadsNew
import roundcube
import roundcubeOutbox
import pidgin
import skype

TARGETS = {
    'twitter' : [
            twitter.TwitterParser(),
            twitter.Output(),
            twitter.TwitterPreProcesser()
        ],
    'facebook' : [
            facebook.FacebookParser(),
            facebook.Output(),
            facebook.FacebookPreProcesser()
        ],
    'facebook_threads' : [
            facebookThreads.FacebookThreadsParser(),
            facebookThreads.Output(),
            facebookThreads.FacebookThreadsPreProcesser()
        ],
    'roundcube' : [
            roundcube.RoundcubeParser(),
            roundcube.Output(),
            roundcube.RoundcubePreProcesser()
        ],
    'roundcube_outbox' : [
            roundcubeOutbox.RoundcubeOutboxParser(),
            roundcubeOutbox.Output(),
            roundcubeOutbox.RoundcubePreProcesser()
        ],
    'pidgin' : [
            pidgin.PidginParser(),
            pidgin.Output(),
            pidgin.PidginPreProcesser()
        ],
    'skype' : [
        skype.SkypeParser(),
        skype.Output(),
        skype.SkypePreProcesser()
    ],
    }
