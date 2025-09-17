import numpy as np
import scipy.sparse as sp
import pytest
from sklearn import svm
X_train = sp.csr_matrix([[0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]])
y_train = np.array([0.04, 0.04, 0.1, 0.16])