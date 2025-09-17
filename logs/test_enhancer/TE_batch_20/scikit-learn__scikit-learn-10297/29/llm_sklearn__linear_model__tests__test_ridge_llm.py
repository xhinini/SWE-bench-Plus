import numpy as np
from sklearn.model_selection import KFold
from sklearn import datasets
from sklearn.utils.testing import assert_true
from sklearn.utils.testing import assert_false
from sklearn.utils.testing import assert_equal
from sklearn.utils.testing import assert_raises
from sklearn.utils.testing import assert_raise_message
from sklearn.linear_model.ridge import RidgeClassifierCV
iris = datasets.load_iris()
X_iris = iris.data
y_iris = iris.target