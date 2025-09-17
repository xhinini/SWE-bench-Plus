import types
from types import ModuleType
import sys
import types
from types import ModuleType
import importlib
import pytest
from sklearn.utils._show_versions import _get_deps_info, _get_sys_info, show_versions, _get_blas_info
import sklearn.utils._show_versions as show_mod
DEPS = ['pip', 'setuptools', 'sklearn', 'numpy', 'scipy', 'Cython', 'pandas', 'matplotlib', 'joblib']