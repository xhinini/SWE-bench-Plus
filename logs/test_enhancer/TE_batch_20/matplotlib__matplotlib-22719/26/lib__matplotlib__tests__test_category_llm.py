import logging
import warnings
import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib._api import MatplotlibDeprecationWarning
import matplotlib.category as cat
LOG_SUBSTR = 'Using categorical units to plot a list of strings'