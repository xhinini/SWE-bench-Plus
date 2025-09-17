import copy
import copy
import numpy as np
import pytest
from numpy.testing import assert_array_equal, assert_array_almost_equal
from astropy.nddata import NDDataRef
from astropy.nddata.mixins.tests.test_ndarithmetic import NDDataArithmetic as _NDDataArithmetic_alias
NDDataArithmetic = NDDataRef