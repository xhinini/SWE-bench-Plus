import sklearn.cluster
import numpy as np
import pytest
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.utils.testing import assert_array_equal, assert_warns_message
import sklearn.cluster