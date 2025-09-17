from sklearn.linear_model.logistic import _log_reg_scoring_path, LogisticRegression
import numpy as np
from sklearn.linear_model.logistic import _log_reg_scoring_path, LogisticRegression
from sklearn.datasets import make_classification
from sklearn.metrics import log_loss, accuracy_score, make_scorer
from sklearn.metrics.scorer import get_scorer
from sklearn.preprocessing import LabelEncoder, LabelBinarizer
import pytest
from sklearn.utils.testing import assert_almost_equal, assert_array_almost_equal, assert_equal
if __name__ == '__main__':
    import pytest
    pytest.main([__file__])