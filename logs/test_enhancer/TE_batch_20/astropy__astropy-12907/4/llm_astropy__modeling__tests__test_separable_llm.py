from astropy.modeling.core import Model
import numpy as np
import pytest
from numpy.testing import assert_allclose
from astropy.modeling.separable import _cstack, _coord_matrix, _cdot