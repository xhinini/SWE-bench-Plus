from unittest import mock
from django.test import SimpleTestCase
from django.db import migrations
from django.db.migrations.writer import MigrationWriter

def _extract_import_lines(output):
    """
    Helper to extract the import lines from the produced migration string,
    in order. We ignore the header comments and blank lines.
    """
    lines = []
    for line in output.splitlines():
        line = line.rstrip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        if line.startswith('class Migration'):
            break
        lines.append(line)
    return [l for l in lines if l.startswith('import ') or l.startswith('from ')]