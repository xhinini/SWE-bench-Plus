pass
import numpy as np
import copy
import pytest
from numpy.testing import assert_array_equal, assert_equal
from astropy.nddata import NDDataRef
from astropy.nddata.mixins.mixarithmetic import NDArithmeticMixin
from astropy.nddata import NDDataRef as NDRefClass
from astropy.nddata.mixins.tests.test_ndarithmetic import NDDataArithmetic
ND = NDDataRef