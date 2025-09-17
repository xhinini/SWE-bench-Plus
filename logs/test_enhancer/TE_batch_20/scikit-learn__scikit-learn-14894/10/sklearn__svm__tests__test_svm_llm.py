import numpy as np
from scipy import sparse
from sklearn import svm
from numpy.testing import assert_allclose
import pytest
import numpy as np
from scipy import sparse
from sklearn import svm
from numpy.testing import assert_array_equal, assert_allclose, assert_array_almost_equal
import pytest
X_train = sparse.csr_matrix([[0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float64)
y_train = np.array([0.04, 0.04, 0.1, 0.16], dtype=np.float64)