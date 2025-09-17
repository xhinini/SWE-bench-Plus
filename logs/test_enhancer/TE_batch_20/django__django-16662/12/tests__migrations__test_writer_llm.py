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

from django.db.migrations.serializer import BaseSerializer
from django.db import migrations
from django.db.migrations.writer import MigrationWriter, OperationWriter
from django.db.migrations.serializer import BaseSerializer
from django.test import SimpleTestCase

def _register_serializer_for(type_, imports_and_string):
    """
    Register a serializer for type_ that returns the provided (string, imports_set).
    imports_and_string: (string, set_of_import_lines)
    """

    class CustomSerializer(BaseSerializer):

        def serialize(self):
            return imports_and_string
    MigrationWriter.register_serializer(type_, CustomSerializer)

def _unregister(type_):
    try:
        MigrationWriter.unregister_serializer(type_)
    except Exception:
        pass