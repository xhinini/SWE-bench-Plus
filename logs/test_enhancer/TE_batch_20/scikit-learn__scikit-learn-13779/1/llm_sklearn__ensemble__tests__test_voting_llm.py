import numpy as np
import pytest
from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.utils.testing import assert_array_almost_equal, assert_array_equal, assert_raise_message
import numpy as np
import pytest
from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.utils.validation import has_fit_parameter
from sklearn.utils.testing import assert_array_almost_equal, assert_array_equal, assert_raise_message