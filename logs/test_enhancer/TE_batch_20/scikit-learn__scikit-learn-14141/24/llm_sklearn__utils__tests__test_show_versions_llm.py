import importlib
import sys
import types
import pytest
import importlib
import sys
import types
import pytest
from sklearn.utils import _show_versions as show_mod
from sklearn.utils._show_versions import _get_sys_info, _get_deps_info, show_versions
EXPECTED_DEPS = ['pip', 'setuptools', 'sklearn', 'numpy', 'scipy', 'Cython', 'pandas', 'matplotlib', 'joblib']