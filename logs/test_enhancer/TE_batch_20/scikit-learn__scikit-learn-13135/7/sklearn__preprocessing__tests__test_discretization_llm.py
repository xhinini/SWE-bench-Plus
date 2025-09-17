import numpy as np
import pytest
import sklearn.cluster as cluster
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.utils.testing import assert_array_equal
from numpy.testing import assert_allclose
import scipy.sparse as sp