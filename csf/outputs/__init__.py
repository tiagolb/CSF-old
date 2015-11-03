import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'

from output import PLATFORM
from output import htmlOutput
from output import textOutput

