import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'

from output import OutputFactory
from output import AUDIT_DIR
from output import time_convert
from output import urldecode
import HTML

