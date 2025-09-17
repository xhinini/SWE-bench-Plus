import numpy as np
import pytest
from sklearn.cluster.optics_ import OPTICS
from sklearn.cluster.dbscan_ import DBSCAN
CASES = [(4, 2, 2.6 / 4.0), (5, 3, 3.6 / 5.0), (6, 2, 2.6 / 6.0), (7, 3, 3.6 / 7.0), (10, 3, 3.6 / 10.0)]