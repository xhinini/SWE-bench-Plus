from django.test import TestCase
from django.forms.models import model_to_dict
from .models import Category, Colour, ColourfulItem, BetterWriter, Writer
from django.test import TestCase
from django.forms.models import model_to_dict
from .models import Category, Colour, ColourfulItem, BetterWriter, Writer

class ModelToDictRegressionTests(TestCase):

    def setUp(self):
        self.cat = Category.objects.create(name='Alpha', slug='alpha', url='alpha-url')
        self.blue = Colour.objects.create(name='blue')
        self.red = Colour.objects.create(name='red')
        self.item = ColourfulItem.objects.create()
        self.item.colours.set([self.blue, self.red])
        self.writer = Writer.objects.create(name='Writer Name')
        self.better = BetterWriter.objects.create(name='Better', score=5)

def test_model_to_dict_with_empty_list_fields_returns_empty(self):
    c = Category.objects.create(name='X', slug='x', url='u')
    self.assertEqual(model_to_dict(c, fields=[]), {})

def test_model_to_dict_with_empty_tuple_fields_returns_empty(self):
    c = Category.objects.create(name='Y', slug='y', url='v')
    self.assertEqual(model_to_dict(c, fields=()), {})

def test_model_to_dict_with_empty_set_fields_returns_empty(self):
    c = Category.objects.create(name='Z', slug='z', url='w')
    self.assertEqual(model_to_dict(c, fields=set()), {})

def test_model_to_dict_with_empty_frozenset_fields_returns_empty(self):
    c = Category.objects.create(name='A', slug='a', url='p')
    self.assertEqual(model_to_dict(c, fields=frozenset()), {})

def test_model_to_dict_with_empty_fields_and_exclude_still_empty(self):
    c = Category.objects.create(name='B', slug='b', url='q')
    self.assertEqual(model_to_dict(c, fields=[], exclude=['name']), {})

def test_model_to_dict_with_empty_fields_on_many_to_many_returns_empty(self):
    blue = Colour.objects.create(name='blue')
    item = ColourfulItem.objects.create(name='item1')
    item.colours.add(blue)
    self.assertEqual(model_to_dict(item, fields=[]), {})

def test_model_to_dict_with_explicit_single_field_returns_only_that_field(self):
    c = Category.objects.create(name='OnlyName', slug='only-name', url='u2')
    self.assertEqual(model_to_dict(c, fields=['name']), {'name': 'OnlyName'})

def test_model_to_dict_with_nonexistent_field_in_fields_returns_empty(self):
    c = Category.objects.create(name='C', slug='c', url='r')
    self.assertEqual(model_to_dict(c, fields=['no_such_field']), {})

def test_model_to_dict_with_empty_fields_for_inherited_model_returns_empty(self):
    bw = BetterWriter.objects.create(name='BW', score=1)
    self.assertEqual(model_to_dict(bw, fields=[]), {})

def test_model_to_dict_fields_none_returns_all_editable_fields(self):
    c = Category.objects.create(name='All', slug='all', url='all-url')
    data = model_to_dict(c, fields=None)
    self.assertCountEqual(list(data.keys()), ['name', 'slug', 'url'])

def test_fields_empty_list_returns_empty_dict(self):
    c = Category.objects.create(name='Cat A', slug='cat-a', url='http://a.example')
    self.assertEqual(model_to_dict(c, fields=[]), {})

def test_fields_empty_tuple_returns_empty_dict(self):
    c = Category.objects.create(name='Cat B', slug='cat-b', url='http://b.example')
    self.assertEqual(model_to_dict(c, fields=()), {})

def test_fields_empty_set_returns_empty_dict(self):
    c = Category.objects.create(name='Cat C', slug='cat-c', url='http://c.example')
    self.assertEqual(model_to_dict(c, fields=set()), {})

def test_fields_empty_frozenset_returns_empty_dict(self):
    c = Category.objects.create(name='Cat D', slug='cat-d', url='http://d.example')
    self.assertEqual(model_to_dict(c, fields=frozenset()), {})

def test_fields_empty_range_returns_empty_dict(self):
    c = Category.objects.create(name='Cat E', slug='cat-e', url='http://e.example')
    self.assertEqual(model_to_dict(c, fields=range(0)), {})

def test_fields_empty_dict_returns_empty_dict(self):
    c = Category.objects.create(name='Cat F', slug='cat-f', url='http://f.example')
    self.assertEqual(model_to_dict(c, fields={}), {})

def test_fields_empty_dict_keys_returns_empty_dict(self):
    c = Category.objects.create(name='Cat G', slug='cat-g', url='http://g.example')
    self.assertEqual(model_to_dict(c, fields={}.keys()), {})

def test_fields_empty_with_exclude_returns_empty_dict(self):
    c = Category.objects.create(name='Cat H', slug='cat-h', url='http://h.example')
    self.assertEqual(model_to_dict(c, fields=[], exclude=['name']), {})

def test_fields_empty_preserves_m2m_when_none(self):
    blue = Colour.objects.create(name='blue-x')
    item = ColourfulItem.objects.create()
    item.colours.set([blue])
    self.assertEqual(model_to_dict(item, fields=None)['colours'], [blue])
    self.assertEqual(model_to_dict(item, fields=[]), {})

def test_empty_fields_on_subclassed_model_returns_empty_dict(self):
    bw = BetterWriter.objects.create(name='BW', score=1)
    self.assertEqual(model_to_dict(bw, fields=[]), {})

from django.test import TestCase
from django.forms.models import model_to_dict
from .models import Writer

class ModelToDictEmptyFieldsRegressionTests(TestCase):

    def setUp(self):
        self.writer = Writer.objects.create(name='John EmptyFields')