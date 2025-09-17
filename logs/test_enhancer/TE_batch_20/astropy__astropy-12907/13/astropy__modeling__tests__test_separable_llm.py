import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_array_equal
from astropy.modeling import models
from astropy.modeling.separable import _cstack, _coord_matrix