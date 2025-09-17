from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS
from astropy.wcs import WCS
import numpy as np
import warnings
from numpy.testing import assert_allclose
from astropy.wcs import WCS
from astropy.io.fits.verify import VerifyWarning
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS
COUPLED_WCS_HEADER = {'WCSAXES': 3, 'CRPIX1': (100 + 1) / 2, 'CRPIX2': (25 + 1) / 2, 'CRPIX3': 1.0, 'PC1_1': 0.0, 'PC1_2': -1.0, 'PC1_3': 0.0, 'PC2_1': 1.0, 'PC2_2': 0.0, 'PC2_3': -1.0, 'CDELT1': 5, 'CDELT2': 5, 'CDELT3': 0.055, 'CUNIT1': 'arcsec', 'CUNIT2': 'arcsec', 'CUNIT3': 'Angstrom', 'CTYPE1': 'HPLN-TAN', 'CTYPE2': 'HPLT-TAN', 'CTYPE3': 'WAVE', 'CRVAL1': 0.0, 'CRVAL2': 0.0, 'CRVAL3': 1.05}
with warnings.catch_warnings():
    warnings.simplefilter('ignore', VerifyWarning)
    FITS_WCS = WCS(header=COUPLED_WCS_HEADER)