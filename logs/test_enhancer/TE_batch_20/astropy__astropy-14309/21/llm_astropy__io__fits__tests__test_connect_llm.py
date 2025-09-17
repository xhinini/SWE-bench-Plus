import io
import numpy as np
import pytest
from astropy.io import fits
from astropy.io.fits import connect, HDUList, BinTableHDU, TableHDU
from astropy.io.fits.hdu.hdulist import FITS_SIGNATURE