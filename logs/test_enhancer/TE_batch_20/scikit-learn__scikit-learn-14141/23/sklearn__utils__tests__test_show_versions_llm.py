import sys
import types
import importlib
from sklearn.utils._show_versions import _get_deps_info, _get_sys_info, _get_blas_info, show_versions
import sklearn._build_utils as _build_utils
import pytest