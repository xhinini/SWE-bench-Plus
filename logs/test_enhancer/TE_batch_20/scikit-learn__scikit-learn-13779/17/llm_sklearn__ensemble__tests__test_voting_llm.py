import numpy as np
import pytest
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.testing import assert_array_equal, assert_array_almost_equal
from sklearn.utils.testing import assert_raise_message