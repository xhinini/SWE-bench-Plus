import numpy as np
import pytest
from sklearn.cluster import k_means, KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics.cluster import v_measure_score
RNG = np.random.RandomState(0)