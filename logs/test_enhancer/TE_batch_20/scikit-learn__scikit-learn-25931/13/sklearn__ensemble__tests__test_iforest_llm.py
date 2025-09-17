from unittest.mock import patch
import pandas as pd
from scipy.sparse import csc_matrix, csr_matrix
import pytest
import numpy as np
import pandas as pd
from scipy.sparse import csc_matrix, csr_matrix
from unittest.mock import patch
from sklearn.ensemble import IsolationForest
from sklearn.datasets import load_iris
iris = load_iris()