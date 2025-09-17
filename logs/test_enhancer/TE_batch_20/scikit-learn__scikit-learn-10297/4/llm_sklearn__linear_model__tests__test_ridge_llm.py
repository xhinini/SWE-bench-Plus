import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model.ridge import RidgeClassifierCV
from sklearn.datasets import make_classification
from sklearn.utils import check_random_state
import numpy as np
from sklearn.model_selection import KFold
from sklearn.utils.testing import assert_raises
from sklearn.utils.testing import assert_raise_message
from sklearn.utils.testing import assert_true
from sklearn.utils.testing import assert_array_equal
from sklearn.utils.testing import assert_array_almost_equal
from sklearn.utils.testing import assert_almost_equal
from sklearn.linear_model.ridge import RidgeClassifierCV, RidgeClassifier
from sklearn.datasets import make_classification
from sklearn.utils import check_random_state
rng = check_random_state(0)