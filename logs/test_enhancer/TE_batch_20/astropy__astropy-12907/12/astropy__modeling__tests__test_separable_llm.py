import numpy as np
import pytest
from numpy.testing import assert_allclose
from astropy.modeling import models
from astropy.modeling.models import Mapping
from astropy.modeling.separable import _cstack, _coord_matrix
from astropy.modeling.core import Model