import numpy as np
import pytest
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import get_scorer
from sklearn.preprocessing import LabelBinarizer
from sklearn.datasets import make_classification
from sklearn.linear_model.logistic import _log_reg_scoring_path, LogisticRegression, logistic_regression_path