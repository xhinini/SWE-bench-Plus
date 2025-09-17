import numpy as np
import pytest
from sklearn.compose import ColumnTransformer, make_column_transformer
try:
    Trans
except NameError:
    from sklearn.base import TransformerMixin, BaseEstimator

    class Trans(TransformerMixin, BaseEstimator):

        def fit(self, X, y=None):
            return self

        def transform(self, X, y=None):
            if hasattr(X, 'to_frame'):
                return X.to_frame()
            if getattr(X, 'ndim', 2) == 1:
                return np.atleast_2d(X).T
            return X