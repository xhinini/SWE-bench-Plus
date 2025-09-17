import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_equal
from astropy.wcs import WCS
import astropy.units as u
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS