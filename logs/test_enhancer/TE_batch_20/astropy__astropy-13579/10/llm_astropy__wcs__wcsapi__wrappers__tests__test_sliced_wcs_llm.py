import warnings
import numpy as np
import pytest
from numpy.testing import assert_allclose
from astropy.io.fits import Header
from astropy.wcs.wcs import WCS
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS
import astropy.units as u
HEADER_SPECTRAL_CUBE = '\nNAXIS   = 3\nNAXIS1  = 10\nNAXIS2  = 20\nNAXIS3  = 30\nCTYPE1  = GLAT-CAR\nCTYPE2  = FREQ\nCTYPE3  = GLON-CAR\nCNAME1  = Latitude\nCNAME2  = Frequency\nCNAME3  = Longitude\nCRVAL1  = 10\nCRVAL2  = 20\nCRVAL3  = 25\nCRPIX1  = 30\nCRPIX2  = 40\nCRPIX3  = 45\nCDELT1  = -0.1\nCDELT2  =  0.5\nCDELT3  =  0.1\nCUNIT1  = deg\nCUNIT2  = Hz\nCUNIT3  = deg\n'