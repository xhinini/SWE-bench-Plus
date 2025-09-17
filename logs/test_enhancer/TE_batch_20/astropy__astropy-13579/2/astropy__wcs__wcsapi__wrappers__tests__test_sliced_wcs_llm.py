import warnings
import numpy as np
from numpy.testing import assert_allclose
from astropy.io.fits import Header
from astropy.io.fits.verify import VerifyWarning
from astropy.wcs import WCS
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS
import warnings
import numpy as np
from numpy.testing import assert_allclose
import pytest
from astropy.io.fits import Header
from astropy.io.fits.verify import VerifyWarning
from astropy.wcs import WCS
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS
HEADER_SPECTRAL_CUBE = '\nNAXIS   = 3\nNAXIS1  = 10\nNAXIS2  = 20\nNAXIS3  = 30\nCTYPE1  = GLAT-CAR\nCTYPE2  = FREQ\nCTYPE3  = GLON-CAR\nCNAME1  = Latitude\nCNAME2  = Frequency\nCNAME3  = Longitude\nCRVAL1  = 10\nCRVAL2  = 20\nCRVAL3  = 25\nCRPIX1  = 30\nCRPIX2  = 40\nCRPIX3  = 45\nCDELT1  = -0.1\nCDELT2  =  0.5\nCDELT3  =  0.1\nCUNIT1  = deg\nCUNIT2  = Hz\nCUNIT3  = deg\n'
CASES = [([slice(None), 10, slice(None)], (29, 10, 44)), ([slice(None), 0, slice(None)], (29, 0, 44)), ([slice(None), 5, slice(None)], (29, 5, 44)), ([0, slice(None), slice(None)], (0, 39, 44)), ([slice(None), slice(None), 0], (29, 39, 0)), ([10, 0, slice(None)], (10, 0, 44)), ([slice(None), 2, 3], (29, 2, 3)), ([3, slice(None), 5], (3, 39, 5)), ([slice(None), slice(None), slice(None)], (29, 39, 44)), ([5, 6, slice(None)], (5, 6, 44))]