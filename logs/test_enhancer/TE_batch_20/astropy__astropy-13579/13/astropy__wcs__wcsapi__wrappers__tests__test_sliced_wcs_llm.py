import numpy as np
from numpy.testing import assert_allclose, assert_equal
import astropy.units as u
from astropy.wcs.wcsapi.wrappers.sliced_wcs import SlicedLowLevelWCS
from astropy.wcs.wcs import WCS
try:
    WCS_SPECTRAL = globals().get('WCS_SPECTRAL_CUBE')
    WCS_SPECTRAL_ROT = globals().get('WCS_SPECTRAL_CUBE_ROT')
    COUPLED_HEADER = globals().get('COUPLED_WCS_HEADER')
except Exception:
    WCS_SPECTRAL = None
    WCS_SPECTRAL_ROT = None
    COUPLED_HEADER = None
if WCS_SPECTRAL is None:
    from astropy.io.fits import Header
    HEADER = '\n    NAXIS = 3\n    NAXIS1 = 10\n    NAXIS2 = 20\n    NAXIS3 = 30\n    CTYPE1 = GLAT-CAR\n    CTYPE2 = FREQ\n    CTYPE3 = GLON-CAR\n    CRVAL1 = 10\n    CRVAL2 = 20\n    CRVAL3 = 25\n    CRPIX1 = 30\n    CRPIX2 = 40\n    CRPIX3 = 45\n    CDELT1 = -0.1\n    CDELT2 = 0.5\n    CDELT3 = 0.1\n    CUNIT1 = deg\n    CUNIT2 = Hz\n    CUNIT3 = deg\n    '
    WCS_SPECTRAL = WCS(Header.fromstring(HEADER, sep='\n'))
    WCS_SPECTRAL.pixel_bounds = [(-1, 11), (-2, 18), (5, 15)]
if WCS_SPECTRAL_ROT is None:
    WCS_SPECTRAL_ROT = WCS_SPECTRAL.deepcopy()
    WCS_SPECTRAL_ROT.wcs.pc = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    WCS_SPECTRAL_ROT.pixel_bounds = WCS_SPECTRAL.pixel_bounds
if COUPLED_HEADER is None:
    COUPLED_HEADER = {'WCSAXES': 3, 'CRPIX1': (100 + 1) / 2, 'CRPIX2': (25 + 1) / 2, 'CRPIX3': 1.0, 'PC1_1': 0.0, 'PC1_2': -1.0, 'PC1_3': 0.0, 'PC2_1': 1.0, 'PC2_2': 0.0, 'PC2_3': -1.0, 'CDELT1': 5, 'CDELT2': 5, 'CDELT3': 0.055, 'CUNIT1': 'arcsec', 'CUNIT2': 'arcsec', 'CUNIT3': 'Angstrom', 'CTYPE1': 'HPLN-TAN', 'CTYPE2': 'HPLT-TAN', 'CTYPE3': 'WAVE', 'CRVAL1': 0.0, 'CRVAL2': 0.0, 'CRVAL3': 1.05}