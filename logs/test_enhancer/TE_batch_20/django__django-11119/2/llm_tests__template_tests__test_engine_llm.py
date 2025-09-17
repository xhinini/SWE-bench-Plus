import os
from django.template import Context
from django.template.engine import Engine
from django.test import SimpleTestCase
from .utils import TEMPLATE_DIR

class TemplateRenderDictRejectionTests(SimpleTestCase):

    def test_template_render_from_string_with_dict_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR], autoescape=True)
        template = engine.from_string('obj:{{ obj }}')
        with self.assertRaises(AttributeError):
            template.render({'obj': '<script>'})

    def test_template_render_get_template_with_dict_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR], autoescape=True)
        template = engine.get_template('test_context.html')
        with self.assertRaises(AttributeError):
            template.render({'obj': '<script>'})

    def test_template_render_from_string_with_dict_autoescape_false_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR], autoescape=False)
        template = engine.from_string('obj:{{ obj }}')
        with self.assertRaises(AttributeError):
            template.render({'obj': '<script>'})

    def test_template_render_get_template_with_dict_autoescape_false_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR], autoescape=False)
        template = engine.get_template('test_context.html')
        with self.assertRaises(AttributeError):
            template.render({'obj': '<script>'})

    def test_template_render_from_string_with_empty_dict_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR])
        template = engine.from_string('x:{{ x }}')
        with self.assertRaises(AttributeError):
            template.render({})

    def test_template_render_get_template_with_non_string_value_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR])
        template = engine.get_template('test_context.html')
        with self.assertRaises(AttributeError):
            template.render(42)

from django.template import Context, Template
from django.template.engine import Engine
from django.test import SimpleTestCase
from .utils import TEMPLATE_DIR

class EngineRegressionTests(SimpleTestCase):

    def setUp(self):
        self.engine = Engine(dirs=[TEMPLATE_DIR])

    def test_template_render_with_dict_raises_attribute_error(self):
        template = Template('{{ name }}')
        with self.assertRaises(AttributeError):
            template.render({'name': 'value'})

    def test_template_render_with_list_raises_attribute_error(self):
        template = Template('{{ name }}')
        with self.assertRaises(AttributeError):
            template.render(['a', 'b'])

    def test_template_render_with_string_raises_attribute_error(self):
        template = Template('{{ name }}')
        with self.assertRaises(AttributeError):
            template.render('not-a-context')

    def test_template_render_with_none_raises_attribute_error(self):
        template = Template('{{ name }}')
        with self.assertRaises(AttributeError):
            template.render(None)

    def test_template_render_with_int_raises_attribute_error(self):
        template = Template('{{ name }}')
        with self.assertRaises(AttributeError):
            template.render(123)

    def test_template_render_with_tuple_raises_attribute_error(self):
        template = Template('{{ name }}')
        with self.assertRaises(AttributeError):
            template.render(('a',))