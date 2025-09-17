from django.utils.safestring import mark_safe
from django.test import SimpleTestCase
from django.utils.safestring import mark_safe
from ..utils import setup

class JsonScriptEdgeCaseTests(SimpleTestCase):

    @setup({'json-empty-literal': '{{ value|json_script:"" }}'})
    def test_empty_string_literal_id_omitted(self):
        output = self.engine.render_to_string('json-empty-literal', {'value': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-var': '{{ value|json_script:element_id }}'})
    def test_empty_string_variable_id_omitted(self):
        output = self.engine.render_to_string('json-empty-var', {'value': {}, 'element_id': ''})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-zero-int': '{{ value|json_script:element_id }}'})
    def test_zero_int_variable_id_omitted(self):
        output = self.engine.render_to_string('json-zero-int', {'value': {}, 'element_id': 0})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-zero-float': '{{ value|json_script:element_id }}'})
    def test_zero_float_variable_id_omitted(self):
        output = self.engine.render_to_string('json-zero-float', {'value': {}, 'element_id': 0.0})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-false-var': '{{ value|json_script:element_id }}'})
    def test_false_variable_id_omitted(self):
        output = self.engine.render_to_string('json-false-var', {'value': {}, 'element_id': False})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-list': '{{ value|json_script:element_id }}'})
    def test_empty_list_variable_id_omitted(self):
        output = self.engine.render_to_string('json-empty-list', {'value': {}, 'element_id': []})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-safe-empty': '{{ value|json_script:element_id }}'})
    def test_mark_safe_empty_string_id_omitted(self):
        output = self.engine.render_to_string('json-safe-empty', {'value': {}, 'element_id': mark_safe('')})
        self.assertEqual(output, '<script type="application/json">{}</script>')