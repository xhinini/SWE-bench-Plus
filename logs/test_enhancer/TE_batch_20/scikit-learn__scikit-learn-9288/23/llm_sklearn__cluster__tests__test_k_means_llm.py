import numpy as np
from scipy import sparse as sp
import pytest
from sklearn.cluster import KMeans, k_means
from sklearn.datasets import make_blobs
from sklearn.utils.testing import assert_allclose, assert_array_equal