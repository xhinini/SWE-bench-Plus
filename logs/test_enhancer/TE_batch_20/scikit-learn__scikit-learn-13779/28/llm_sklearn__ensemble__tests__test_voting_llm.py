from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
import pytest
import numpy as np
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.dummy import DummyRegressor
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
X_small = np.array([[0.0], [1.0], [2.0], [3.0]])
y_small = np.array([0, 0, 1, 1])