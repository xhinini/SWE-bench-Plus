import numpy as np
from numpy.testing import assert_allclose
import pytest
from astropy.wcs import WCS
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS
from astropy.wcs.wcsapi.wrappers.sliced_wcs import sanitize_slices, combine_slices
from astropy.wcs.wcs import FITSFixedWarning
from astropy.io.fits.verify import VerifyWarning
from astropy.io.fits import Header
from astropy.coordinates import SkyCoord, Galactic, ICRS
import astropy.units as u
COUPLED_WCS_HEADER = {'WCSAXES': 3, 'CRPIX1': (100 + 1) / 2, 'CRPIX2': (25 + 1) / 2, 'CRPIX3': 1.0, 'PC1_1': 0.0, 'PC1_2': -1.0, 'PC1_3': 0.0, 'PC2_1': 1.0, 'PC2_2': 0.0, 'PC2_3': -1.0, 'CDELT1': 5, 'CDELT2': 5, 'CDELT3': 0.055, 'CUNIT1': 'arcsec', 'CUNIT2': 'arcsec', 'CUNIT3': 'Angstrom', 'CTYPE1': 'HPLN-TAN', 'CTYPE2': 'HPLT-TAN', 'CTYPE3': 'WAVE', 'CRVAL1': 0.0, 'CRVAL2': 0.0, 'CRVAL3': 1.05}