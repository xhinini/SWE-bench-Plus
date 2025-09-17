import numpy as np
import pytest
from sklearn.ensemble import IsolationForest
from sklearn.utils import check_random_state
'\nAdditional regression tests for IsolationForest warm_start handling.\nThese tests target the bug fixed by forwarding warm_start to BaseBagging.\n'