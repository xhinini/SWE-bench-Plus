import pytest
import numpy as np
from io import BytesIO
from astropy.io import fits
from astropy.io.fits import connect, HDUList, BinTableHDU, ImageHDU, PrimaryHDU, TableHDU
from astropy.io.fits.hdu.hdulist import FITS_SIGNATURE