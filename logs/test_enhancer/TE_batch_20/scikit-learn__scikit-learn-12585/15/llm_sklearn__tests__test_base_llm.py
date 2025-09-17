import numpy as np
from sklearn.utils.testing import assert_raises, assert_equal
from sklearn.base import clone, BaseEstimator
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV