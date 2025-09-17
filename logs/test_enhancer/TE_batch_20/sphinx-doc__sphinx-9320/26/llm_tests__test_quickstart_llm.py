import os
import tempfile
import shutil
from io import StringIO
import pytest
from sphinx.cmd import quickstart as qs
from sphinx.cmd.quickstart import ValidationError