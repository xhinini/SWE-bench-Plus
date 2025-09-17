import pytest
import numpy as np
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.utils.testing import assert_equal, assert_raises, assert_raise_message
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris