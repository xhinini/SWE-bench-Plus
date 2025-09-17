import numpy as np
from scipy import sparse
from sklearn import svm
import numpy as np
import pytest
from scipy import sparse
from sklearn import svm
X_train = sparse.csr_matrix([[0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]])
y_train = np.array([0.04, 0.04, 0.1, 0.16])