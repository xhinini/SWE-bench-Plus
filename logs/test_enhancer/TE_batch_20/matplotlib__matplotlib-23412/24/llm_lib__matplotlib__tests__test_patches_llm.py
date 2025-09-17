import contextlib
import pytest
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib import cbook
line_styles = [(0, [6, 6]), (3, [6, 6]), (6, [6, 6]), (0, [2, 2, 6, 2]), (4, [2, 2, 6, 2]), (0, [10, 5, 2, 5]), (5, [10, 5, 2, 5]), (0, [1, 3]), (2, [1, 3]), (7, [4, 1, 4, 1])]