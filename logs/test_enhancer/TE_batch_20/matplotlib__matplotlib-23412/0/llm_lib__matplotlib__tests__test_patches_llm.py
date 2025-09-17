import contextlib
from contextlib import contextmanager
import pytest
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.path import Path
import contextlib
from contextlib import contextmanager
import numpy as np
import pytest
import matplotlib.patches as mpatches
from matplotlib.path import Path
CASES = [(make_rectangle, (0, [6, 6]), (5, [3, 3])), (make_polygon, (0, [4, 2]), (7, [2, 2])), (make_pathpatch, (2, [1, 1]), (9, [5, 5])), (make_wedge, (0, [8, 3]), (3, [6, 6])), (make_circle, (4, [5, 5]), (1, [2, 2])), (make_ellipse, (0, [10, 2]), (6, [4, 4])), (make_regularpolygon, (1, [3, 7]), (8, [1, 1])), (make_fancybbox, (0, [2, 2]), (11, [6, 6])), (make_fancyarrow, (0, [6, 6]), (5, [9, 1])), (make_arrow, (3, [3, 3]), (12, [2, 4]))]