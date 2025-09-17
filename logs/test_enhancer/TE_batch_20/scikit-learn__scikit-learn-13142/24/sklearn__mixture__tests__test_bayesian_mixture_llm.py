import copy
import numpy as np
import pytest
from sklearn.mixture import GaussianMixture
from sklearn.exceptions import ConvergenceWarning
from sklearn.utils.testing import assert_array_equal
from sklearn.utils.testing import ignore_warnings