import numpy as np
import pytest
from scipy import sparse as sp
from sklearn.cluster import KMeans, k_means
from sklearn.datasets import make_blobs
from sklearn.metrics.cluster import v_measure_score
from numpy.testing import assert_allclose