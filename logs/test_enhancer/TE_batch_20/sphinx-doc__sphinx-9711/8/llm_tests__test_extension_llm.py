"""
    test_extension (additional regression tests)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Additional tests to cover version comparison edge cases and legacy-version
    requirement strings for verify_needs_extensions.
"""
import pytest
from sphinx.errors import VersionRequirementError
from sphinx.extension import Extension, verify_needs_extensions