"""
Regression tests for astropy.modeling.separable._cstack when operands are
numpy arrays. These tests ensure that numeric values from ndarray operands
are preserved (not replaced with ones).
"""
import numpy as np
import pytest
from numpy.testing import assert_array_equal, assert_allclose
from astropy.modeling import models
from astropy.modeling.models import Mapping
from astropy.modeling.separable import _cstack, _compute_n_outputs, _coord_matrix
sh1 = models.Shift(1, name='shift1')
rot = models.Rotation2D(2, name='rotation')