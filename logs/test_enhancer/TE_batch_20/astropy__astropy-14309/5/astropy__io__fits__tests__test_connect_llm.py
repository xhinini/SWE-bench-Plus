import io
import pytest
from astropy.io import fits
from astropy.io.fits import connect
from astropy.io.fits import HDUList, TableHDU, BinTableHDU, GroupsHDU, PrimaryHDU
from astropy.io.fits.hdu.hdulist import FITS_SIGNATURE