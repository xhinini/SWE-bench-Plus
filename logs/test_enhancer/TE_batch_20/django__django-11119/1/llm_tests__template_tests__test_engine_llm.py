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