"""
    test_extension_regressions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Regression tests for version checking in sphinx.extension.verify_needs_extensions.

    These tests create a minimal mock app and Config instance and call
    verify_needs_extensions to assert whether a VersionRequirementError is raised.
"""
import pytest
from sphinx.config import Config
from sphinx.errors import VersionRequirementError
from sphinx.extension import Extension, verify_needs_extensions