"""
    test_ext_viewcode_singlehtml
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Regression tests for sphinx.ext.viewcode collect_pages early-return
    behavior for the "singlehtml" builder.
"""
import pytest
from pathlib import Path