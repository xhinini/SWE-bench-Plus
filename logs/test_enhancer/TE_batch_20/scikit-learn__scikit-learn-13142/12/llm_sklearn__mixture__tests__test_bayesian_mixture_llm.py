import numpy as np
import pytest
from sklearn.datasets import make_blobs
from sklearn.mixture import GaussianMixture
from sklearn.exceptions import ConvergenceWarning
from sklearn.utils.testing import assert_array_equal