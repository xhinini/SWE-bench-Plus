import numpy as np
import scipy.sparse as sp
from sklearn.metrics import get_scorer
import numpy as np
import scipy.sparse as sp
import pytest
from sklearn.linear_model import logistic as logistic_module
from sklearn.linear_model.logistic import _log_reg_scoring_path
X_small = np.array([[0.1, 1.1], [1.2, 0.2], [2.1, 1.9], [3.0, 2.5], [0.5, 0.3]])
y_three = np.array([0, 1, 2, 1, 0])
train_idx = np.array([0, 1, 2, 3])
test_idx = np.array([4])