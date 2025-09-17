import numpy as np
import pytest
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.utils._joblib import Memory
from sklearn.tests.test_pipeline import Transf, Mult, FitParamT, DummyTransf