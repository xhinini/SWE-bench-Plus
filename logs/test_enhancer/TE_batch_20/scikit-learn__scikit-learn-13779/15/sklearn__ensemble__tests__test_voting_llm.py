from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin
import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyRegressor
from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.utils.testing import assert_array_almost_equal, assert_array_equal
from sklearn.utils.testing import assert_raise_message
X_clf = np.array([[0.0], [1.0], [2.0], [3.0]])
y_clf = np.array([0, 0, 1, 1])
X_reg = np.array([[0.0], [1.0], [2.0], [3.0]])
y_reg = np.array([0.0, 1.0, 2.0, 3.0])