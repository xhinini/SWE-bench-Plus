import numpy as np
import scipy.sparse as sparse
import pytest
from sklearn import svm
import numpy as np
import scipy.sparse as sparse
import pytest
from sklearn import svm
from sklearn.utils import check_random_state
from sklearn.exceptions import NotFittedError
rng = check_random_state(0)
X_train = sparse.csr_matrix([[0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float64)
y_reg = np.array([0.04, 0.04, 0.1, 0.16])
X_test = np.array([[0, 1, 0, 0], [0, 0, 1, 0]], dtype=np.float64)