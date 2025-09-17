import numpy as np
from numpy.testing import assert_allclose
import pytest
from matplotlib import mlab
import numpy as np
from numpy.testing import assert_allclose
import pytest
from matplotlib import mlab
WIN_REAL_NEG = np.array([1.0, -0.5, 0.8, -0.3, 0.6, -0.2, 0.4, -0.1])
X_SMALL = np.arange(len(WIN_REAL_NEG)).astype(float)
WIN_COMPLEX = WIN_REAL_NEG + 1j * np.linspace(0.1, 0.8, len(WIN_REAL_NEG))
X_SMALL_REAL = X_SMALL.copy()