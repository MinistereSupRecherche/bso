import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from doi_utils import *
from elsevier import *
from springer import *
from nature import *
from generic import *
from wiley import *
from openedition import *
from cairn import *
from aanda import *
from acs import *
from aps import *
from bmc import *
from iop import *
from frontiers import *
from rsc import *
from plos import *
from cambridge import *
from mdpi import *
from oup import *
from aip import *
from spie import *
from atmos_chem import *
from bmj import *
from sagepub import *
from erudit import *
from ssrn import *
from sciendo import *
from ios import *
from pubmed import *
from ieee import *
from acm import *

from global_html_parser import *
