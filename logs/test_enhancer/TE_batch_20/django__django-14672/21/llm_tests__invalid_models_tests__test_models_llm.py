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

from django.db.models.fields.reverse_related import ManyToManyRel
from django.test import SimpleTestCase
from django.db.models.fields.reverse_related import ManyToManyRel

class ManyToManyRelIdentityTests(SimpleTestCase):

    def setUp(self):
        self.dummy_field = object()
        self.dummy_to = object()

    def test_none_and_empty_tuple_not_equal(self):
        rel_none = ManyToManyRel(self.dummy_field, self.dummy_to, through='through_model', through_fields=None, db_constraint=True)
        rel_empty_tuple = ManyToManyRel(self.dummy_field, self.dummy_to, through='through_model', through_fields=(), db_constraint=True)
        self.assertNotEqual(rel_none, rel_empty_tuple)

    def test_none_and_empty_list_not_equal(self):
        rel_none = ManyToManyRel(self.dummy_field, self.dummy_to, through='through_model', through_fields=None, db_constraint=True)
        rel_empty_list = ManyToManyRel(self.dummy_field, self.dummy_to, through='through_model', through_fields=[], db_constraint=True)
        self.assertNotEqual(rel_none, rel_empty_list)

from django.test import SimpleTestCase
from django.db.models.fields.reverse_related import ManyToManyRel

class ManyToManyRelIdentityTests(SimpleTestCase):

    def _make_rel(self, through=None, through_fields=None):
        field = object()
        to = object()
        return ManyToManyRel(field, to, through=through, through_fields=through_fields)

from django.db.models.fields.reverse_related import ManyToManyRel
from django.test import SimpleTestCase
from django.db.models.fields.reverse_related import ManyToManyRel

class ManyToManyRelIdentityTests(SimpleTestCase):

    def test_empty_list_vs_none_not_equal(self):
        field = object()
        rel_none = self.make_rel(field, through=None, through_fields=None)
        rel_empty_list = self.make_rel(field, through=None, through_fields=[])
        self.assertNotEqual(rel_none, rel_empty_list)
        self.assertNotEqual(hash(rel_none), hash(rel_empty_list))

    def test_empty_tuple_vs_none_not_equal(self):
        field = object()
        rel_none = self.make_rel(field, through=None, through_fields=None)
        rel_empty_tuple = self.make_rel(field, through=None, through_fields=())
        self.assertNotEqual(rel_none, rel_empty_tuple)
        self.assertNotEqual(hash(rel_none), hash(rel_empty_tuple))

    def test_set_contains_both_none_and_empty_list(self):
        field = object()
        rel_none = self.make_rel(field, through=None, through_fields=None)
        rel_empty_list = self.make_rel(field, through=None, through_fields=[])
        s = {rel_none, rel_empty_list}
        self.assertEqual(len(s), 2)
        self.assertIn(rel_none, s)
        self.assertIn(rel_empty_list, s)

    def test_dict_keys_distinguish_none_and_empty_tuple(self):
        field = object()
        rel_none = self.make_rel(field, through=None, through_fields=None)
        rel_empty_tuple = self.make_rel(field, through=None, through_fields=())
        d = {rel_none: 'none', rel_empty_tuple: 'empty_tuple'}
        self.assertEqual(d[rel_none], 'none')
        self.assertEqual(d[rel_empty_tuple], 'empty_tuple')
        self.assertEqual(len(d), 2)

    def test_empty_list_is_not_cast_to_none(self):
        field = object()
        rel_none = self.make_rel(field, through='T', through_fields=None)
        rel_empty_list = self.make_rel(field, through='T', through_fields=[])
        self.assertNotEqual(rel_none, rel_empty_list)
        self.assertNotEqual(hash(rel_none), hash(rel_empty_list))

from django.utils.hashable import make_hashable
from django.db.models.fields.reverse_related import ManyToManyRel
import unittest
from django.utils.hashable import make_hashable
from django.db.models.fields.reverse_related import ManyToManyRel

class ManyToManyRelIdentityTests(unittest.TestCase):

    def setUp(self):
        self.field = object()
        self.Model = type('DummyModel', (), {})
        self.Through = type('ThroughModel', (), {})
        self.r_with_empty = ManyToManyRel(field=self.field, to=self.Model, through=self.Through, through_fields=[])
        self.r_with_none = ManyToManyRel(field=self.field, to=self.Model, through=self.Through, through_fields=None)

    def test_relations_are_not_equal(self):
        self.assertNotEqual(self.r_with_empty, self.r_with_none)

    def test_hash_values_are_different(self):
        self.assertNotEqual(hash(self.r_with_empty), hash(self.r_with_none))

    def test_set_contains_two_distinct_relations(self):
        s = {self.r_with_empty, self.r_with_none}
        self.assertEqual(len(s), 2)
        self.assertIn(self.r_with_empty, s)
        self.assertIn(self.r_with_none, s)

    def test_identity_contains_hashable_through_fields_for_empty_list(self):
        self.assertEqual(self.r_with_empty.identity[-2], make_hashable([]))

    def test_dict_keys_distinct(self):
        d = {}
        d[self.r_with_empty] = 'empty'
        d[self.r_with_none] = 'none'
        self.assertEqual(len(d), 2)
        self.assertEqual(d[self.r_with_empty], 'empty')
        self.assertEqual(d[self.r_with_none], 'none')

    def test_list_indexing_preserves_order(self):
        lst = [self.r_with_empty, self.r_with_none]
        self.assertEqual(lst.index(self.r_with_empty), 0)
        self.assertEqual(lst.index(self.r_with_none), 1)

    def test_relation_not_in_set_of_other(self):
        s = {self.r_with_empty}
        self.assertNotIn(self.r_with_none, s)

    def test_dict_update_keeps_both_keys(self):
        d = {}
        d[self.r_with_empty] = 1
        d[self.r_with_none] = 2
        self.assertEqual(len(d), 2)
        self.assertEqual(d[self.r_with_empty], 1)
        self.assertEqual(d[self.r_with_none], 2)

    def test_counts_in_list(self):
        lst = [self.r_with_empty, self.r_with_none]
        self.assertEqual(lst.count(self.r_with_empty), 1)
        self.assertEqual(lst.count(self.r_with_none), 1)

import unittest
from django.db.models.fields.reverse_related import ManyToManyRel

def build_rel(field=None, to=None, through=None, through_fields=None, db_constraint=True):
    return ManyToManyRel(field or object(), to or DummyModel, related_name='relname', related_query_name='rq', limit_choices_to=None, symmetrical=False, through=through, through_fields=through_fields, db_constraint=db_constraint)
if __name__ == '__main__':
    unittest.main()

from django.test import SimpleTestCase
from django.test.utils import isolate_apps
from django.utils.hashable import make_hashable
from django.db.models.fields.reverse_related import ManyToManyRel

@isolate_apps('invalid_models_tests')
class ManyToManyRelIdentityTests(SimpleTestCase):

    def _dummy_field(self):
        return object()

from django.db.models.fields.reverse_related import ManyToManyRel
import unittest
from django.db.models.fields.reverse_related import ManyToManyRel

class ManyToManyRelIdentityTests(unittest.TestCase):

    def setUp(self):
        self.field = object()
        self.model = object()

    def make_rel(self, through=None, through_fields=None, db_constraint=True):
        return ManyToManyRel(self.field, self.model, related_name='r', related_query_name='rq', through=through, through_fields=through_fields, db_constraint=db_constraint)

    def test_none_not_equal_empty_list(self):
        rel_none = self.make_rel(through='T', through_fields=None)
        rel_empty_list = self.make_rel(through='T', through_fields=[])
        self.assertNotEqual(rel_none, rel_empty_list)
        self.assertNotEqual(hash(rel_none), hash(rel_empty_list))

    def test_none_not_equal_empty_tuple(self):
        rel_none = self.make_rel(through='T', through_fields=None)
        rel_empty_tuple = self.make_rel(through='T', through_fields=())
        self.assertNotEqual(rel_none, rel_empty_tuple)
        self.assertNotEqual(hash(rel_none), hash(rel_empty_tuple))

    def test_set_membership_distinguishes_none_and_empty_list(self):
        rel_none = self.make_rel(through='T', through_fields=None)
        rel_empty_list = self.make_rel(through='T', through_fields=[])
        s = {rel_none, rel_empty_list}
        self.assertEqual(len(s), 2)
        self.assertIn(rel_none, s)
        self.assertIn(rel_empty_list, s)

    def test_dict_keys_distinguish_none_and_empty_tuple(self):
        rel_none = self.make_rel(through='T', through_fields=None)
        rel_empty_tuple = self.make_rel(through='T', through_fields=())
        d = {rel_none: 'none'}
        self.assertNotIn(rel_empty_tuple, d)
        with self.assertRaises(KeyError):
            _ = d[rel_empty_tuple]

from django.test import SimpleTestCase
from django.db.models.fields.reverse_related import ManyToManyRel

class ManyToManyRelIdentityTests(SimpleTestCase):

    def setUp(self):
        self.field = object()
        self.model = object()

    def test_through_fields_empty_list_hashed_to_empty_tuple(self):
        rel = self.make_rel([])
        self.assertEqual(rel.identity[-2], ())

    def test_identity_none_and_empty_list_different(self):
        rel_none = self.make_rel(None)
        rel_empty = self.make_rel([])
        self.assertNotEqual(rel_none.identity, rel_empty.identity)
        self.assertFalse(rel_none == rel_empty)
        self.assertNotEqual(hash(rel_none), hash(rel_empty))

    def test_set_contains_both_none_and_empty_list(self):
        rel_none = self.make_rel(None)
        rel_empty = self.make_rel([])
        s = {rel_none, rel_empty}
        self.assertEqual(len(s), 2)

    def test_dict_keys_distinct_for_none_and_empty_list(self):
        rel_none = self.make_rel(None)
        rel_empty = self.make_rel([])
        d = {rel_none: 'none', rel_empty: 'empty'}
        self.assertEqual(len(d), 2)
        self.assertEqual(d[rel_none], 'none')
        self.assertEqual(d[rel_empty], 'empty')

    def test_identity_with_through_model_empty_list(self):
        through_model = object()
        rel = self.make_rel([], through=through_model)
        self.assertIs(rel.identity[-3], through_model)
        self.assertEqual(rel.identity[-2], ())
        self.assertIs(rel.identity[-1], True)