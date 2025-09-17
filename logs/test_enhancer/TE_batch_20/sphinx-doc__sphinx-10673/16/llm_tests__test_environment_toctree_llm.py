"""Tests for skipping generated documents in assign_figure_numbers."""
import pytest
from docutils import nodes
from sphinx import addnodes
from sphinx.environment.collectors.toctree import TocTreeCollector