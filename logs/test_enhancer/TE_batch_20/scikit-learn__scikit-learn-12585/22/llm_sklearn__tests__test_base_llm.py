import collections
from sklearn.base import BaseEstimator, clone
from sklearn.svm import SVC
from sklearn.utils.testing import assert_raises, assert_true, assert_equal