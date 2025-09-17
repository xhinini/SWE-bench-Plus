import importlib
import numpy as np
import scipy.sparse as sp
from sklearn.metrics.cluster import fowlkes_mallows_score
from sklearn.utils import assert_all_finite
import importlib
import numpy as np
import scipy.sparse as sp
from sklearn.metrics.cluster import fowlkes_mallows_score
from sklearn.utils import assert_all_finite
sup = importlib.import_module('sklearn.metrics.cluster.supervised')