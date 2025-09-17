import types
import importlib
import sys
import sys
import importlib
import types
from collections import Counter
from sklearn.utils._show_versions import _get_deps_info, _get_sys_info, show_versions
EXPECTED_DEPS_ORDER = ['pip', 'setuptools', 'sklearn', 'numpy', 'scipy', 'Cython', 'pandas', 'matplotlib', 'joblib']