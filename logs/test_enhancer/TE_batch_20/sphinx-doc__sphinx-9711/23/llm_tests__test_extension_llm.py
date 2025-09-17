"""
    test_extension_additional
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Additional regression tests for sphinx.extension.verify_needs_extensions.
"""
import pytest
from packaging.version import Version, InvalidVersion
from sphinx.errors import VersionRequirementError
from sphinx.extension import Extension, verify_needs_extensions