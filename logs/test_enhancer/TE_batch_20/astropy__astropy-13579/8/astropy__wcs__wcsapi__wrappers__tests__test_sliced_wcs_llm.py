import numpy as np
from numpy.testing import assert_allclose
import astropy.units as u
import pytest
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS
from astropy.wcs.wcs import WCS
try:
    WCS_SPECTRAL_CUBE
except NameError:
    from astropy.io.fits import Header
    HEADER_SPECTRAL_CUBE = '\n    NAXIS   = 3\n    NAXIS1  = 10\n    NAXIS2  = 20\n    NAXIS3  = 30\n    CTYPE1  = GLAT-CAR\n    CTYPE2  = FREQ\n    CTYPE3  = GLON-CAR\n    CRVAL1  = 10\n    CRVAL2  = 20\n    CRVAL3  = 25\n    CRPIX1  = 30\n    CRPIX2  = 40\n    CRPIX3  = 45\n    CDELT1  = -0.1\n    CDELT2  =  0.5\n    CDELT3  =  0.1\n    CUNIT1  = deg\n    CUNIT2  = Hz\n    CUNIT3  = deg\n    '
    from astropy.io.fits import Header
    WCS_SPECTRAL_CUBE = WCS(Header.fromstring(HEADER_SPECTRAL_CUBE, sep='\n'))
    WCS_SPECTRAL_CUBE.pixel_bounds = [(-1, 11), (-2, 18), (5, 15)]