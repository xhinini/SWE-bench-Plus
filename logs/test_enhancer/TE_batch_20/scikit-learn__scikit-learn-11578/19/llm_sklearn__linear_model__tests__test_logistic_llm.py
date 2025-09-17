from sklearn.metrics import log_loss
from sklearn.preprocessing import LabelEncoder
import numpy as np
import scipy.sparse as sp
import pytest
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import log_loss
from sklearn.metrics.scorer import get_scorer, make_scorer
from sklearn.linear_model.logistic import _log_reg_scoring_path, LogisticRegression
from sklearn.preprocessing import LabelEncoder