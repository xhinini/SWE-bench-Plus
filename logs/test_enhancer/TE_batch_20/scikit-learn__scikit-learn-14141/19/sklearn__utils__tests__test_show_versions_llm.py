import importlib
import sys
import types
import pytest
import sys
import types
import importlib
import pytest
from importlib import reload
mod = importlib.import_module('sklearn.utils._show_versions')
_get_deps_info = mod._get_deps_info
show_versions = mod.show_versions
EXPECTED_DEPS = ['pip', 'setuptools', 'sklearn', 'numpy', 'scipy', 'Cython', 'pandas', 'matplotlib', 'joblib']