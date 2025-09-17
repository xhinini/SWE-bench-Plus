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

from decimal import Decimal
from django.test import SimpleTestCase
from ..utils import setup

class JsonScriptFalsyIdTests(SimpleTestCase):

    @setup({'json-tag-empty-lit': '{{ value|json_script:"" }}'})
    def test_empty_string_literal_no_id(self):
        output = self.engine.render_to_string('json-tag-empty-lit', {'value': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-var': '{{ value|json_script:element_id }}'})
    def test_zero_numeric_no_id(self):
        output = self.engine.render_to_string('json-tag-var', {'value': {}, 'element_id': 0})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-var': '{{ value|json_script:element_id }}'})
    def test_false_no_id(self):
        output = self.engine.render_to_string('json-tag-var', {'value': {}, 'element_id': False})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-var': '{{ value|json_script:element_id }}'})
    def test_empty_list_no_id(self):
        output = self.engine.render_to_string('json-tag-var', {'value': {}, 'element_id': []})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-var': '{{ value|json_script:element_id }}'})
    def test_empty_tuple_no_id(self):
        output = self.engine.render_to_string('json-tag-var', {'value': {}, 'element_id': ()})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-var': '{{ value|json_script:element_id }}'})
    def test_empty_dict_no_id(self):
        output = self.engine.render_to_string('json-tag-var', {'value': {}, 'element_id': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-var': '{{ value|json_script:element_id }}'})
    def test_empty_set_no_id(self):
        output = self.engine.render_to_string('json-tag-var', {'value': {}, 'element_id': set()})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-var': '{{ value|json_script:element_id }}'})
    def test_empty_bytes_no_id(self):
        output = self.engine.render_to_string('json-tag-var', {'value': {}, 'element_id': b''})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-var': '{{ value|json_script:element_id }}'})
    def test_decimal_zero_no_id(self):
        from decimal import Decimal
        output = self.engine.render_to_string('json-tag-var', {'value': {}, 'element_id': Decimal(0)})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-var': '{{ value|json_script:element_id }}'})
    def test_float_zero_no_id(self):
        output = self.engine.render_to_string('json-tag-var', {'value': {}, 'element_id': 0.0})
        self.assertEqual(output, '<script type="application/json">{}</script>')

from django.test import SimpleTestCase
from ..utils import setup
from django.test import SimpleTestCase
from ..utils import setup

class JsonScriptTests(SimpleTestCase):

    @setup({'json-tag03': '{{ value|json_script:"" }}'})
    def test_empty_string_literal_omits_id(self):
        output = self.engine.render_to_string('json-tag03', {'value': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag04': '{{ value|json_script:id }}'})
    def test_empty_string_variable_omits_id(self):
        output = self.engine.render_to_string('json-tag04', {'value': {}, 'id': ''})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag05': '{{ value|json_script:id }}'})
    def test_false_variable_omits_id(self):
        output = self.engine.render_to_string('json-tag05', {'value': {}, 'id': False})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag06': '{{ value|json_script:id }}'})
    def test_empty_list_variable_omits_id(self):
        output = self.engine.render_to_string('json-tag06', {'value': {}, 'id': []})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag07': '{{ value|json_script:id }}'})
    def test_zero_integer_variable_omits_id(self):
        output = self.engine.render_to_string('json-tag07', {'value': {}, 'id': 0})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag10': '{{ value|json_script:id }}'})
    def test_special_chars_value_with_empty_id(self):
        value = {'a': 'testing\r\njson \'string" <b>escaping</b>'}
        output = self.engine.render_to_string('json-tag10', {'value': value, 'id': ''})
        self.assertEqual(output, '<script type="application/json">{"a": "testing\\r\\njson \'string\\" \\u003Cb\\u003Eescaping\\u003C/b\\u003E"}</script>')

from django.test import SimpleTestCase
from ..utils import setup

class JsonScriptRegressionTests(SimpleTestCase):

    @setup({'t_empty_literal': '{{ value|json_script:"" }}'})
    def test_empty_string_literal_omits_id(self):
        output = self.engine.render_to_string('t_empty_literal', {'value': {'a': 1}})
        self.assertEqual(output, '<script type="application/json">{"a": 1}</script>')

    @setup({'t_empty_variable': '{{ value|json_script:element_id }}'})
    def test_empty_string_variable_omits_id(self):
        output = self.engine.render_to_string('t_empty_variable', {'value': {'a': 1}, 'element_id': ''})
        self.assertEqual(output, '<script type="application/json">{"a": 1}</script>')

    @setup({'t_zero_int': '{{ value|json_script:element_id }}'})
    def test_zero_integer_omits_id(self):
        output = self.engine.render_to_string('t_zero_int', {'value': {'a': 1}, 'element_id': 0})
        self.assertEqual(output, '<script type="application/json">{"a": 1}</script>')

    @setup({'t_false_boolean': '{{ value|json_script:element_id }}'})
    def test_false_boolean_omits_id(self):
        output = self.engine.render_to_string('t_false_boolean', {'value': {'a': 1}, 'element_id': False})
        self.assertEqual(output, '<script type="application/json">{"a": 1}</script>')

    @setup({'t_empty_list': '{{ value|json_script:element_id }}'})
    def test_empty_list_omits_id(self):
        output = self.engine.render_to_string('t_empty_list', {'value': {'a': 1}, 'element_id': []})
        self.assertEqual(output, '<script type="application/json">{"a": 1}</script>')

    @setup({'t_zero_float': '{{ value|json_script:element_id }}'})
    def test_zero_float_omits_id(self):
        output = self.engine.render_to_string('t_zero_float', {'value': {'a': 1}, 'element_id': 0.0})
        self.assertEqual(output, '<script type="application/json">{"a": 1}</script>')

from django.test import SimpleTestCase
from ..utils import setup

class JsonScriptAdditionalTests(SimpleTestCase):

    @setup({'json-no-id-literal': '{{ value|json_script:"" }}'})
    def test_empty_string_id_literal_no_id(self):
        output = self.engine.render_to_string('json-no-id-literal', {'value': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-no-id-variable': '{{ value|json_script:id }}'})
    def test_empty_string_id_variable_no_id(self):
        output = self.engine.render_to_string('json-no-id-variable', {'value': {}, 'id': ''})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-false-id': '{{ value|json_script:id }}'})
    def test_false_id_variable_no_id(self):
        output = self.engine.render_to_string('json-false-id', {'value': {}, 'id': False})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-zero-id': '{{ value|json_script:id }}'})
    def test_zero_id_variable_no_id(self):
        output = self.engine.render_to_string('json-zero-id', {'value': {}, 'id': 0})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-emptylist-id': '{{ value|json_script:id }}'})
    def test_empty_list_id_variable_no_id(self):
        output = self.engine.render_to_string('json-emptylist-id', {'value': {}, 'id': []})
        self.assertEqual(output, '<script type="application/json">{}</script>')

from django.test import SimpleTestCase
from ..utils import setup

class JsonScriptTests(SimpleTestCase):

    @setup({'json-tag-empty-string': '{{ value|json_script:element_id }}'})
    def test_empty_string_id(self):
        output = self.engine.render_to_string('json-tag-empty-string', {'value': {}, 'element_id': ''})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-zero-int': '{{ value|json_script:element_id }}'})
    def test_zero_int_id(self):
        output = self.engine.render_to_string('json-tag-zero-int', {'value': {}, 'element_id': 0})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-false': '{{ value|json_script:element_id }}'})
    def test_false_id(self):
        output = self.engine.render_to_string('json-tag-false', {'value': {}, 'element_id': False})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-empty-list': '{{ value|json_script:element_id }}'})
    def test_empty_list_id(self):
        output = self.engine.render_to_string('json-tag-empty-list', {'value': {}, 'element_id': []})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-empty-tuple': '{{ value|json_script:element_id }}'})
    def test_empty_tuple_id(self):
        output = self.engine.render_to_string('json-tag-empty-tuple', {'value': {}, 'element_id': ()})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-tag-empty-dict': '{{ value|json_script:element_id }}'})
    def test_empty_dict_id(self):
        output = self.engine.render_to_string('json-tag-empty-dict', {'value': {}, 'element_id': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

from decimal import Decimal
from django.test import SimpleTestCase
from decimal import Decimal
from ..utils import setup


class JsonScriptFalsyIdTests(SimpleTestCase):

    @setup({'json-empty-literal': '{{ value|json_script:"" }}'})
    def test_empty_string_literal(self):
        output = self.engine.render_to_string('json-empty-literal', {'value': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-var': '{{ value|json_script:eid }}'})
    def test_empty_string_variable(self):
        output = self.engine.render_to_string('json-empty-var', {'value': {}, 'eid': ''})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-false-var': '{{ value|json_script:eid }}'})
    def test_false_variable(self):
        output = self.engine.render_to_string('json-false-var', {'value': {}, 'eid': False})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-zero-var': '{{ value|json_script:eid }}'})
    def test_zero_variable(self):
        output = self.engine.render_to_string('json-zero-var', {'value': {}, 'eid': 0})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-list': '{{ value|json_script:eid }}'})
    def test_empty_list_variable(self):
        output = self.engine.render_to_string('json-empty-list', {'value': {}, 'eid': []})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-tuple': '{{ value|json_script:eid }}'})
    def test_empty_tuple_variable(self):
        output = self.engine.render_to_string('json-empty-tuple', {'value': {}, 'eid': ()})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-dict': '{{ value|json_script:eid }}'})
    def test_empty_dict_variable(self):
        output = self.engine.render_to_string('json-empty-dict', {'value': {}, 'eid': {}})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-set': '{{ value|json_script:eid }}'})
    def test_empty_set_variable(self):
        output = self.engine.render_to_string('json-empty-set', {'value': {}, 'eid': set()})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-empty-bytes': '{{ value|json_script:eid }}'})
    def test_empty_bytes_variable(self):
        output = self.engine.render_to_string('json-empty-bytes', {'value': {}, 'eid': b''})
        self.assertEqual(output, '<script type="application/json">{}</script>')

    @setup({'json-decimal-zero': '{{ value|json_script:eid }}'})
    def test_decimal_zero_variable(self):
        output = self.engine.render_to_string('json-decimal-zero', {'value': {}, 'eid': Decimal(0)})
        self.assertEqual(output, '<script type="application/json">{}</script>')