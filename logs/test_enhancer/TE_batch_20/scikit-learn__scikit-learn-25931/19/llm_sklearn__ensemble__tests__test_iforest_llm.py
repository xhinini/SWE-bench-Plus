import numpy as np
import pytest
from scipy.sparse import csc_matrix, csr_matrix
import pandas as pd
from unittest.mock import patch
from sklearn.ensemble import IsolationForest