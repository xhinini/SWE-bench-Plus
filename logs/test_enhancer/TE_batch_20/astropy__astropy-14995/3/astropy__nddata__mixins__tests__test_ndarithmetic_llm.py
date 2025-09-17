import copy
import numpy as np
import pytest
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_equal
from astropy.nddata import NDDataRef as NDDataArithmetic
import astropy.nddata.mixins.tests.test_ndarithmetic as base_tests