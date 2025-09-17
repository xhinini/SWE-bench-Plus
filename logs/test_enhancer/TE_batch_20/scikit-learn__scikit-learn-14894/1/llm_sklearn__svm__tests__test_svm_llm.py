import numpy as np
from scipy import sparse
import pytest
from sklearn import svm
import numpy as np
import pytest
from scipy import sparse
from sklearn import svm
X_train_sparse = sparse.csr_matrix([[0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]])
X_train_dense = X_train_sparse.toarray()
y_train = np.array([0.04, 0.04, 0.1, 0.16])
n_features = X_train_dense.shape[1]