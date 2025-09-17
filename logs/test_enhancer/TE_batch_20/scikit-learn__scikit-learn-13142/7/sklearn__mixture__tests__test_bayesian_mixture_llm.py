import numpy as np
import pytest
from sklearn.utils.testing import assert_array_equal
from sklearn.mixture.base import BaseMixture
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from scipy.special import logsumexp