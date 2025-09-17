"""
    test_ext_viewcode_singlehtml
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Regression tests for sphinx.ext.viewcode ensuring that the singlehtml
    builder does not generate separate module pages or a _modules directory.

    These tests assert absence of _modules output and absence of links to
    module pages in the produced index pages.
"""
import pytest
import os