from django.db.models.fields.reverse_related import ManyToManyRel
import types
from django.test import SimpleTestCase
from django.db.models.fields.reverse_related import ManyToManyRel
import types

class ManyToManyRelIdentityTests(SimpleTestCase):

    def setUp(self):
        self.field = DummyField()
        self.model = types.SimpleNamespace(__name__='testmodel')

from django.db.models.fields.reverse_related import ManyToManyRel
import unittest
from django.db.models.fields.reverse_related import ManyToManyRel

def _make_stub_field():
    return object()

def _make_stub_model():
    return type('StubModel', (), {'_meta': type('opts', (), {'app_label': 'app', 'model_name': 'stub'})})

def _create_rel(through=None, through_fields=None, db_constraint=True):
    return ManyToManyRel(field=_make_stub_field(), to=_make_stub_model(), related_name='relname', related_query_name='relquery', limit_choices_to=None, symmetrical=True, through=through, through_fields=through_fields, db_constraint=db_constraint)