import pytest
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyRegressor
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.utils.testing import assert_array_equal, assert_array_almost_equal
from sklearn.utils.testing import assert_raise_message
X_small = np.array([[-1.1, -1.5], [-1.2, -1.4], [1.1, 1.2], [2.1, 1.4]])
y_small = np.array([0, 0, 1, 1])