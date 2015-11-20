import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'

import twitter
import facebook
from facebookThreads import *

TARGETS = {
    'twitter' : [
            twitter.TwitterParser(),
            twitter.Output(),
        ],
    'facebook' : [
            facebook.FacebookParser(),
            facebook.Output(),
        ],
    'facebook_threads' : [
            facebookThreads.FacebookThreadsParser(),
            facebookThreads.Output(),
        ],
    }
