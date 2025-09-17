import copy
from sklearn.datasets import make_blobs
from sklearn.utils.testing import assert_array_equal, ignore_warnings
from sklearn.exceptions import ConvergenceWarning
import copy
import numpy as np
import pytest
from sklearn.datasets import make_blobs
from sklearn.utils.testing import assert_array_equal, ignore_warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
X, y_true = make_blobs(n_samples=300, centers=3, n_features=2, cluster_std=0.5, random_state=0)