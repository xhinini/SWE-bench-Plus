"""
    test_extension_regressions
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Regression tests for sphinx.extension.verify_needs_extensions focusing on
    version comparison edge cases (multi-digit parts, prerelease/postrelease,
    build metadata, unknown and legacy versions).
"""
import pytest
from sphinx.errors import VersionRequirementError
from sphinx.extension import Extension, verify_needs_extensions