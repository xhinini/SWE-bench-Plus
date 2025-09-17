import numpy as np
import scipy.sparse as sp
import pytest
from numpy.testing import assert_array_equal, assert_allclose, assert_array_almost_equal
from sklearn import svm
from sklearn.utils import check_random_state