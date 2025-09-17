import sys
import importlib
from types import SimpleNamespace, ModuleType
import pytest
from sklearn.utils import _show_versions as showmod
from sklearn.utils._show_versions import _get_sys_info, _get_deps_info, _get_blas_info, show_versions
EXPECTED_DEPS = {'pip', 'setuptools', 'sklearn', 'numpy', 'scipy', 'Cython', 'pandas', 'matplotlib', 'joblib'}