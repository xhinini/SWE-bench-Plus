import numpy as np
from sklearn.base import clone, BaseEstimator
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.utils.testing import assert_equal, assert_true, assert_false, assert_raises