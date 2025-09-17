"""
    test_ext_viewcode_singlehtml
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Regression tests ensuring viewcode does not generate module pages for
    the singlehtml builder (should return early).
"""
import os
from pathlib import Path
import pytest
from sphinx.ext.viewcode import collect_pages
from sphinx.application import Sphinx