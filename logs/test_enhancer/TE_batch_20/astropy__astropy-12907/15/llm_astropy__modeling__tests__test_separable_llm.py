import numpy as np
from numpy.testing import assert_allclose
from astropy.modeling import models
from astropy.modeling.separable import _cstack, _coord_matrix
sh1 = models.Shift(1)
rot = models.Rotation2D(2)
scl1 = models.Scale(1)