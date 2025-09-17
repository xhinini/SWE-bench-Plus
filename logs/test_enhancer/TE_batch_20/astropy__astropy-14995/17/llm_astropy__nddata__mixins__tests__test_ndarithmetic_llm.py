import numpy as np
import pytest
from numpy.testing import assert_array_equal, assert_array_equal as np_assert_equal
from astropy.nddata import NDDataRef
from astropy.nddata.mixins.ndarithmetic import NDArithmeticMixin
from astropy.nddata.mixins.ndarithmetic import np as _np
ND = NDDataRef