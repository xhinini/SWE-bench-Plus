import numpy as np
import pytest
from numpy.testing import assert_array_equal, assert_allclose
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.dummy import DummyRegressor