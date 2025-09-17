import numpy as np
from scipy import sparse as sp
import importlib
from sklearn.metrics.cluster import fowlkes_mallows_score
supervised = importlib.import_module('sklearn.metrics.cluster.supervised')
from sklearn.utils.testing import assert_all_finite
from numpy.testing import assert_almost_equal, assert_equal
import numpy as np
from scipy import sparse as sp
import importlib
from sklearn.metrics.cluster import fowlkes_mallows_score
supervised = importlib.import_module('sklearn.metrics.cluster.supervised')
from sklearn.utils.testing import assert_all_finite
from numpy.testing import assert_almost_equal, assert_equal