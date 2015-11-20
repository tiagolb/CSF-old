import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'

import twitter
import facebook
import facebookThreads
import roundcube
import roundcubeOutbox
import pidgin

TARGETS = {
    'twitter' : [
            twitter.TwitterParser(),
            twitter.Output(),
            "DirectMessage",
        ],
    'facebook' : [
            facebook.FacebookParser(),
            facebook.Output(),
            "fbid",
        ],
    'facebook_threads' : [
            facebookThreads.FacebookThreadsParser(),
            facebookThreads.Output(),
            None,
        ],
    'roundcube' : [
            roundcube.RoundcubeParser(),
            roundcube.Output(),
        ],
    'roundcube_outbox' : [
            roundcubeOutbox.RoundcubeOutboxParser(),
            roundcubeOutbox.Output(),
        ], 
    'pidgin' : [
        pidgin.PidginParser(),
        pidgin.Output(),
    ],     
    }
