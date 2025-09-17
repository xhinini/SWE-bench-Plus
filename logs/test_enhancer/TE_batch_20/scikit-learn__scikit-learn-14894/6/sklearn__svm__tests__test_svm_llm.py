import numpy as np
import pytest
from scipy import sparse
from sklearn import svm
import numpy as np
import pytest
from scipy import sparse
from sklearn import svm
from numpy.testing import assert_allclose, assert_array_equal
X_train = sparse.csr_matrix([[0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]])
y_train_reg = np.array([0.04, 0.04, 0.1, 0.16])