import pytest
import numpy as np
from sklearn.exceptions import NotFittedError
from sklearn.utils.testing import assert_array_almost_equal, assert_array_equal
from sklearn.utils.testing import assert_raise_message
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
X_small = np.array([[0.0], [1.0], [2.0], [3.0]])
y_class = np.array([0, 0, 1, 1])
y_reg = np.array([0.0, 0.1, 0.9, 1.0])
sample_weight = np.ones(len(y_class))