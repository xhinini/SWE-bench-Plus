import numpy as np
import pytest
from numpy.testing import assert_allclose
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS
from astropy.wcs.wcs import WCS
from astropy.io.fits import Header
from astropy.io.fits.verify import VerifyWarning
import warnings
HEADER_SPECTRAL_CUBE = '\nNAXIS   = 3\nNAXIS1  = 10\nNAXIS2  = 20\nNAXIS3  = 30\nCTYPE1  = GLAT-CAR\nCTYPE2  = FREQ\nCTYPE3  = GLON-CAR\nCNAME1  = Latitude\nCNAME2  = Frequency\nCNAME3  = Longitude\nCRVAL1  = 10\nCRVAL2  = 20\nCRVAL3  = 25\nCRPIX1  = 30\nCRPIX2  = 40\nCRPIX3  = 45\nCDELT1  = -0.1\nCDELT2  =  0.5\nCDELT3  =  0.1\nCUNIT1  = deg\nCUNIT2  = Hz\nCUNIT3  = deg\n'
with warnings.catch_warnings():
    warnings.simplefilter('ignore', VerifyWarning)
    WCS_SPECTRAL_CUBE = WCS(Header.fromstring(HEADER_SPECTRAL_CUBE, sep='\n'))
WCS_SPECTRAL_CUBE.pixel_bounds = [(-1, 11), (-2, 18), (5, 15)]
SLICE_CASES = [[slice(None), 10], np.s_[:, 0, :], np.s_[0, :, :], np.s_[:, 2:5, :], np.s_[slice(2, None), slice(None), slice(None)], np.s_[:, slice(3, 16), :], np.s_[5, :5, 12], np.s_[:, 0, 0], np.s_[2, :, 0], np.s_[slice(None, 10), slice(None, 16), slice(None)]]