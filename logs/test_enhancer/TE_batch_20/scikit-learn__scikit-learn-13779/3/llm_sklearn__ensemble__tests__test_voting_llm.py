import pytest
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.dummy import DummyRegressor