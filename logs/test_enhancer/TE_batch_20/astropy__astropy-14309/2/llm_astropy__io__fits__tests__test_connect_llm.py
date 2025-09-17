import io
import numpy as np
import pytest
from astropy.io.fits import connect, HDUList, BinTableHDU, TableHDU, GroupsHDU, PrimaryHDU
import io
import numpy as np
import pytest
from astropy.io.fits import connect, HDUList, BinTableHDU, TableHDU, GroupsHDU, PrimaryHDU
SAMPLE = np.array([(1,)], dtype=[('a', 'i4')])