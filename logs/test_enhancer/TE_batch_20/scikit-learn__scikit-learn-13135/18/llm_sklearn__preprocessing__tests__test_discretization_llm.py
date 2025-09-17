import pytest
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer, OneHotEncoder
from sklearn.utils.testing import assert_array_equal
import pytest
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer, OneHotEncoder
from sklearn.utils.testing import assert_array_equal
X_single = np.array([0, 0.5, 2, 3, 9, 10]).reshape(-1, 1)