import numpy as np
import scipy.sparse as sp
import warnings
import sklearn.cluster as cluster
import pytest
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.utils.testing import assert_array_equal