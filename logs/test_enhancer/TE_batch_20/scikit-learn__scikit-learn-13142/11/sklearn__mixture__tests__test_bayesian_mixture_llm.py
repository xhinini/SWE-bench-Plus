import numpy as np
import pytest
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from sklearn.exceptions import ConvergenceWarning
from sklearn.utils.testing import assert_array_equal
import warnings