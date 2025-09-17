from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
import numpy as np
import pytest
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.utils.testing import assert_array_equal, assert_array_almost_equal, assert_raise_message
X_clf = np.array([[0.0, 1.0], [1.0, 0.0], [0.5, 0.5], [1.0, 1.0]])
y_clf = np.array([0, 0, 1, 1])
X_reg = np.array([[0.0], [1.0], [2.0], [3.0]])
y_reg = np.array([0.0, 1.0, 2.0, 3.0])