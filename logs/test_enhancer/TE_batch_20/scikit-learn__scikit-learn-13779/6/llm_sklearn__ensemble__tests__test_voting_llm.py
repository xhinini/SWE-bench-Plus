import numpy as np
import pytest
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
X_small = np.array([[0.0], [1.0], [2.0], [3.0]])
y_clf = np.array([0, 0, 1, 1])
y_reg = np.array([0.0, 1.0, 2.0, 3.0])