import pytest
from docutils import nodes
from sphinx import addnodes
from sphinx.addnodes import compact_paragraph
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment.adapters.toctree import TocTree
from sphinx.environment.collectors.toctree import TocTreeCollector