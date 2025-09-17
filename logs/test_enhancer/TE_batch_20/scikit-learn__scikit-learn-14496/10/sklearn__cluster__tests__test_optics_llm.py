import numpy as np
import pytest
from sklearn.cluster.optics_ import OPTICS
from sklearn.utils.testing import assert_array_equal
try:
    rng
except NameError:
    import numpy as _np
    rng = _np.random.RandomState(0)