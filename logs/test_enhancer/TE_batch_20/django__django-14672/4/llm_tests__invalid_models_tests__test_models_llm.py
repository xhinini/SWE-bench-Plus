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

from django.test import SimpleTestCase
from django.db.models.fields.reverse_related import ManyToManyRel

class ManyToManyRelIdentityTests(SimpleTestCase):

    def make_field(self):
        return object()

    def make_model(self):
        return object()

    def make_through(self, name='Through'):
        return type(name, (), {})

    def test_none_vs_empty_tuple_are_different(self):
        field = self.make_field()
        model = self.make_model()
        through = self.make_through('T2')
        rel_none = ManyToManyRel(field, model, through=through, through_fields=None)
        rel_empty = ManyToManyRel(field, model, through=through, through_fields=())
        self.assertNotEqual(rel_none, rel_empty)
        self.assertNotEqual(hash(rel_none), hash(rel_empty))