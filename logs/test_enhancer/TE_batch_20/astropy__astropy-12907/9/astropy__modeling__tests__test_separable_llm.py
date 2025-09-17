"""
Additional regression tests for astropy.modeling.separable._cstack to ensure
that when the right (or left) operand is an ndarray the actual array values
are preserved rather than being filled with ones (bug fixed by patch).
"""
import numpy as np
import pytest
from numpy.testing import assert_allclose
from astropy.modeling import models
from astropy.modeling.separable import _cstack, _coord_matrix
sh1 = models.Shift(1)
rot = models.Rotation2D(2)