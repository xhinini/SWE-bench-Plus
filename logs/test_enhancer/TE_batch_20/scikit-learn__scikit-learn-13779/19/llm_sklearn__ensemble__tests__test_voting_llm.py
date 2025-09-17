import pytest
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier, VotingRegressor, RandomForestClassifier
from sklearn.dummy import DummyRegressor
from sklearn.utils.testing import assert_array_equal, assert_array_almost_equal
from sklearn.exceptions import NotFittedError