import numpy as np
import scipy.sparse as sp
import pytest
from sklearn.datasets import make_classification
from sklearn.metrics import log_loss
from sklearn.metrics.scorer import get_scorer
from sklearn.linear_model.logistic import _log_reg_scoring_path, LogisticRegression