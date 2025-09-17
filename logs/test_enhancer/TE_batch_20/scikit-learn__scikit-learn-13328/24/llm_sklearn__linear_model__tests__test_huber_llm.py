import numpy as np
import pytest
from scipy import sparse
from sklearn.datasets import make_regression
from sklearn.linear_model import HuberRegressor
rng = np.random.RandomState(0)