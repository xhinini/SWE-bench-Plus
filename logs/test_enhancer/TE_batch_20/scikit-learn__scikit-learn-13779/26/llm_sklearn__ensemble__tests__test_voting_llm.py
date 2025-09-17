import numpy as np
import pytest
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.testing import assert_array_equal, assert_array_almost_equal
from sklearn.utils.testing import assert_raise_message, assert_equal
from sklearn.dummy import DummyRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier, VotingRegressor
try:
    X_small = X
    y_small = y
except NameError:
    X_small = np.array([[-1.1, -1.5], [-1.2, -1.4], [1.1, 1.2], [2.1, 1.4]])
    y_small = np.array([0, 0, 1, 1])