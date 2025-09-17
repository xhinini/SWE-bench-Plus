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

from django.test import TestCase
from django.db import transaction
from django.db.models.deletion import Collector
from .models import User, Avatar, Base, M, Parent, Child, HiddenUser, A, R

class FastDeletePkRegressionTests(TestCase):

    def test_avatar_instance_delete_sets_pk_none_when_unreferenced(self):
        a = Avatar.objects.create(desc='unused')
        self._skip_unless_fast_deletable(a)
        result = a.delete()
        self.assertIsNone(a.pk)
        self.assertGreaterEqual(result[0], 1)

    def test_model_with_simple_relation_delete_sets_pk_none(self):
        h = HiddenUser.objects.create(r=R.objects.create())
        self._skip_unless_fast_deletable(h)
        result = h.delete()
        self.assertIsNone(h.pk)
        self.assertGreaterEqual(result[0], 1)

    def test_m_model_instance_delete_sets_pk_none(self):
        m = M.objects.create()
        self._skip_unless_fast_deletable(m)
        result = m.delete()
        self.assertIsNone(m.pk)
        self.assertGreaterEqual(result[0], 1)

    def test_parent_model_instance_delete_sets_pk_none_when_fast(self):
        p = Parent.objects.create()
        self._skip_unless_fast_deletable(p)
        result = p.delete()
        self.assertIsNone(p.pk)
        self.assertGreaterEqual(result[0], 1)

    def test_child_model_simple_instance_delete_sets_pk_none_when_fast(self):
        c = Child.objects.create()
        self._skip_unless_fast_deletable(c)
        result = c.delete()
        self.assertIsNone(c.pk)
        self.assertGreaterEqual(result[0], 1)

from django.db import connection, models
from django.db import transaction
from django.db.models import signals
from django.test import TestCase

def make_model(name, fields=None):
    """
    Dynamically create a model class and its table in the test database.
    `fields` is a dict of name: Field instances (e.g. {'id': models.CharField(...)}).
    """
    attrs = {'__module__': 'tests.dynamic_models'}
    if fields:
        attrs.update(fields)

    class Meta:
        app_label = 'tests'
    attrs['Meta'] = Meta
    Model = type(name, (models.Model,), attrs)
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Model)
    return Model