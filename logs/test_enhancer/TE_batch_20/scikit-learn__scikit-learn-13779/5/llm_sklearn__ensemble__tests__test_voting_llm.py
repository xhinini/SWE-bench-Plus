import numpy as np
import pytest
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyRegressor
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.testing import assert_array_equal, assert_array_almost_equal, assert_raise_message, assert_equal