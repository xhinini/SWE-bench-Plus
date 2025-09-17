from django.db import connection, models
import uuid
from django.test import TestCase
from django.db import models, connection
import uuid

def make_model(name, fields):
    """
    Create a dynamic model class and its database table.
    `fields` should be a dict of field_name: FieldInstance (no primary key
    unless specified in fields).
    """
    attrs = {'__module__': __name__}

    class Meta:
        app_label = 'test_app'
    attrs['Meta'] = Meta
    attrs.update(fields)
    Model = type(name, (models.Model,), attrs)
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Model)
    return Model