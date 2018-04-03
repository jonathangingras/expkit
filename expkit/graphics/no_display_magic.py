import matplotlib as mpl
from matplotlib import rcParams
import os
if os.uname().sysname == 'Linux' and 'DISPLAY' not in os.environ.keys():
    mpl.use('Agg')
    rcParams.update({'figure.autolayout': True})
