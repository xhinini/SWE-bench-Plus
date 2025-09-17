from io import BytesIO
import numpy as np
from astropy.io.fits import connect, HDUList, TableHDU, BinTableHDU, GroupsHDU
from astropy.io.fits.hdu.hdulist import FITS_SIGNATURE
import numpy as np
import pytest
from io import BytesIO
from astropy.io import fits
from astropy.io.fits import connect, HDUList, TableHDU, BinTableHDU, GroupsHDU
from astropy.io.fits.hdu.hdulist import FITS_SIGNATURE