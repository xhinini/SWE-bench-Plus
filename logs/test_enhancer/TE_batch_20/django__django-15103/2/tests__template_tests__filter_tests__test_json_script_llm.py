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

from django.test import SimpleTestCase
from ..utils import setup
from django.test import SimpleTestCase
from ..utils import setup

class JsonScriptRegressionTests(SimpleTestCase):

    @setup({'json-empty-literal': '{{ value|json_script:"" }}'})
    def test_empty_string_literal_omits_id(self):
        output = self.engine.render_to_string('json-empty-literal', {'value': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-var': '{{ value|json_script:element }}'})
    def test_empty_string_variable_omits_id(self):
        output = self.engine.render_to_string('json-empty-var', {'value': {}, 'element': ''})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-false-var': '{{ value|json_script:element }}'})
    def test_false_variable_omits_id(self):
        output = self.engine.render_to_string('json-false-var', {'value': {}, 'element': False})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-zero-int-var': '{{ value|json_script:element }}'})
    def test_zero_integer_variable_omits_id(self):
        output = self.engine.render_to_string('json-zero-int-var', {'value': {}, 'element': 0})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-zero-float-var': '{{ value|json_script:element }}'})
    def test_zero_float_variable_omits_id(self):
        output = self.engine.render_to_string('json-zero-float-var', {'value': {}, 'element': 0.0})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-list-var': '{{ value|json_script:element }}'})
    def test_empty_list_variable_omits_id(self):
        output = self.engine.render_to_string('json-empty-list-var', {'value': {}, 'element': []})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-dict-var': '{{ value|json_script:element }}'})
    def test_empty_dict_variable_omits_id(self):
        output = self.engine.render_to_string('json-empty-dict-var', {'value': {}, 'element': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-tuple-var': '{{ value|json_script:element }}'})
    def test_empty_tuple_variable_omits_id(self):
        output = self.engine.render_to_string('json-empty-tuple-var', {'value': {}, 'element': ()})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-string-with-other': 'x{{ value|json_script:element }}y'})
    def test_empty_string_surrounded_text_omits_id(self):
        output = self.engine.render_to_string('json-empty-string-with-other', {'value': {}, 'element': ''})
        self.assertEqual(output, 'x<script type="application/json">{}</script>y')

# No new imports required (reuses existing imports in the test module).
from django.test import SimpleTestCase

from ..utils import setup


class JsonScriptFalsyIdTests(SimpleTestCase):
    @setup({'json-empty-literal': '{{ value|json_script:"" }}'})
    def test_empty_string_literal_has_no_id(self):
        output = self.engine.render_to_string('json-empty-literal', {'value': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-var': '{{ value|json_script:element }}'})
    def test_empty_string_variable_has_no_id(self):
        output = self.engine.render_to_string('json-empty-var', {'value': {}, 'element': ''})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-zero-literal': '{{ value|json_script:0 }}'})
    def test_zero_literal_has_no_id(self):
        output = self.engine.render_to_string('json-zero-literal', {'value': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-zero-var': '{{ value|json_script:element }}'})
    def test_zero_variable_has_no_id(self):
        output = self.engine.render_to_string('json-zero-var', {'value': {}, 'element': 0})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-zero-float-var': '{{ value|json_script:element }}'})
    def test_zero_float_variable_has_no_id(self):
        output = self.engine.render_to_string('json-zero-float-var', {'value': {}, 'element': 0.0})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-false-var': '{{ value|json_script:element }}'})
    def test_false_variable_has_no_id(self):
        output = self.engine.render_to_string('json-false-var', {'value': {}, 'element': False})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-list-var': '{{ value|json_script:element }}'})
    def test_empty_list_variable_has_no_id(self):
        output = self.engine.render_to_string('json-empty-list-var', {'value': {}, 'element': []})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-dict-var': '{{ value|json_script:element }}'})
    def test_empty_dict_variable_has_no_id(self):
        output = self.engine.render_to_string('json-empty-dict-var', {'value': {}, 'element': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-tuple-var': '{{ value|json_script:element }}'})
    def test_empty_tuple_variable_has_no_id(self):
        output = self.engine.render_to_string('json-empty-tuple-var', {'value': {}, 'element': ()})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-bytes-var': '{{ value|json_script:element }}'})
    def test_empty_bytes_variable_has_no_id(self):
        output = self.engine.render_to_string('json-empty-bytes-var', {'value': {}, 'element': b''})
        self.assertEqual(output, '<script type="application/json">{}</script>')