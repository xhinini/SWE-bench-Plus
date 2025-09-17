import copy
import numpy as np
from sklearn.utils.testing import assert_array_equal
from sklearn.utils.testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from sklearn.mixture.base import BaseMixture
import copy
import numpy as np
from sklearn.utils.testing import assert_array_equal
from sklearn.utils.testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from sklearn.mixture.base import BaseMixture
from scipy.special import logsumexp