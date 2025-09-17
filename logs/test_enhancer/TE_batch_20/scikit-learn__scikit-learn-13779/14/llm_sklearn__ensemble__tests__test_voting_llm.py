import pytest
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyRegressor
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.testing import assert_array_equal, assert_array_almost_equal, assert_equal
from sklearn.utils.testing import assert_raise_message
try:
    from sklearn.datasets import load_iris, load_boston
    iris = load_iris()
    X, y = (iris.data[:, 1:3], iris.target)
    boston = load_boston()
    X_r, y_r = (boston.data, boston.target)
except Exception:
    X = np.array([[0.1, 1.0], [1.1, 2.0], [0.9, 0.8], [1.3, 1.5]])
    y = np.array([0, 1, 0, 1])
    X_r = np.array([[1.0], [2.0], [3.0], [4.0]])
    y_r = np.array([1.0, 2.0, 3.0, 4.0])