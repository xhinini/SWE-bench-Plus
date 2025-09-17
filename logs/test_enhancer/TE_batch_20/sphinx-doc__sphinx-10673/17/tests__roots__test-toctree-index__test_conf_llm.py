import types
import logging
import re
import pytest
from sphinx import addnodes
from sphinx.directives.other import TocTree, url_re, explicit_title_re, glob_re
import sphinx.directives.other as other_mod