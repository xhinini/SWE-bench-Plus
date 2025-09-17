import re
from sklearn import set_config
from sklearn.base import BaseEstimator
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.utils._pprint import _EstimatorPrettyPrinter