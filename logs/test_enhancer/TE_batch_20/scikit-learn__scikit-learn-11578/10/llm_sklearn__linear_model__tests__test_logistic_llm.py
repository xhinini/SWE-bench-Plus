import numpy as np
import scipy.sparse as sp
import pytest
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics.scorer import get_scorer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model.logistic import _log_reg_scoring_path