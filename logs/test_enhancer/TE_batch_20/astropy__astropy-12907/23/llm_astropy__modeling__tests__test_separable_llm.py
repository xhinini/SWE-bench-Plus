import numpy as np
from numpy.testing import assert_allclose
import pytest
from astropy.modeling import models
from astropy.modeling.models import Mapping
from astropy.modeling.core import Model
from astropy.modeling.separable import _coord_matrix, _cstack
sh1 = models.Shift(1)
sh2 = models.Shift(2)
rot = models.Rotation2D(2)
p2 = models.Polynomial2D(1)
p1 = models.Polynomial1D(1)
map1 = Mapping((0, 1, 0, 1))
map2 = Mapping((0, 0, 1))
map3 = Mapping((0, 0))