import numpy as np
import scipy.sparse as sparse
import pytest
from sklearn.datasets import make_regression
from sklearn.linear_model import HuberRegressor
import sklearn.linear_model.huber as hubermod
import numpy as np
import scipy.sparse as sparse
import pytest
from sklearn.datasets import make_regression
from sklearn.linear_model import HuberRegressor
import sklearn.linear_model.huber as hubermod
X_dense, y_dense = make_regression(n_samples=20, n_features=3, random_state=0)