from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
import numpy as np
import pytest
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.dummy import DummyRegressor