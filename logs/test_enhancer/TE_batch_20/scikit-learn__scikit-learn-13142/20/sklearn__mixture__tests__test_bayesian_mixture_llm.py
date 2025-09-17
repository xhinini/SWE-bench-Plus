import numpy as np
import pytest
from sklearn.utils.testing import assert_array_equal
from sklearn.mixture.base import BaseMixture
'\nTests to ensure fit_predict returns labels consistent with the fitted model\nparameters (i.e., predict after fit/fir_predict should return the same labels).\nThe FakeMixture is a minimal concrete implementation of BaseMixture to\ndeterministically exercise the EM loop and initializations.\n'
from math import log, pi