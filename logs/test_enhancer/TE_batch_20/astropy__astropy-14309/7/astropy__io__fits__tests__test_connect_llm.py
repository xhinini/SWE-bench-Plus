from io import BytesIO
from astropy.io.fits.hdu.hdulist import FITS_SIGNATURE
import io
from io import BytesIO
import numpy as np
import pytest
from astropy.io import fits
from astropy.io.fits import BinTableHDU, HDUList, PrimaryHDU, connect
from astropy.io.fits.hdu.hdulist import FITS_SIGNATURE