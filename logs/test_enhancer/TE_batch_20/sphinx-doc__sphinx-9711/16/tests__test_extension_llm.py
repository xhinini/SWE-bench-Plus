"""
Additional regression tests for sphinx.extension.verify_needs_extensions
"""
import pytest
from sphinx.errors import VersionRequirementError
from sphinx.extension import Extension, verify_needs_extensions