import pandas as pd
import warnings
import numpy as np
import pytest
from sklearn.ensemble import IsolationForest
from sklearn.utils._testing import assert_allclose, assert_array_equal
from sklearn.utils import check_random_state
pd = pytest.importorskip('pandas')