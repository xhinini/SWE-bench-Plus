import inspect
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import KFold
import inspect
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import KFold
from sklearn.utils.testing import assert_true
from sklearn.utils.testing import assert_almost_equal
from sklearn.utils.testing import assert_array_almost_equal
from sklearn.utils.testing import assert_equal
from sklearn.utils.testing import assert_array_equal
from sklearn.utils.testing import assert_raises
from sklearn.utils.testing import assert_raise_message
from sklearn.linear_model.ridge import RidgeClassifierCV, RidgeCV