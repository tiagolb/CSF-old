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
