import os
import sys
from io import StringIO
from pathlib import Path
import pytest
from sphinx.cmd import quickstart as qs
from sphinx.cmd.quickstart import ValidationError
real_term_input = qs.term_input