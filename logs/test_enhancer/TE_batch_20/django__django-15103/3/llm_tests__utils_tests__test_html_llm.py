def test_json_script_empty_string_id(self):
    self.assertEqual(json_script('a', ''), '<script type="application/json">"a"</script>')

def test_json_script_zero_id(self):
    self.assertEqual(json_script('a', 0), '<script type="application/json">"a"</script>')

def test_json_script_false_id(self):
    self.assertEqual(json_script('a', False), '<script type="application/json">"a"</script>')

def test_json_script_empty_list_id(self):
    self.assertEqual(json_script('a', []), '<script type="application/json">"a"</script>')

def test_json_script_string_zero_id(self):
    self.assertEqual(json_script('a', '0'), '<script id="0" type="application/json">"a"</script>')

def test_json_script_integer_id(self):
    self.assertEqual(json_script('a', 1), '<script id="1" type="application/json">"a"</script>')

def test_json_script_mark_safe_id(self):
    self.assertEqual(json_script('a', mark_safe('good')), '<script id="good" type="application/json">"a"</script>')

def test_json_script_lazystr_id(self):
    self.assertEqual(json_script('a', lazystr('lazyid')), '<script id="lazyid" type="application/json">"a"</script>')

def test_json_script_escaped_id(self):
    self.assertEqual(json_script('a', '<bad>'), '<script id="&lt;bad&gt;" type="application/json">"a"</script>')

def test_json_script_space_id(self):
    self.assertEqual(json_script('a', ' '), '<script id=" " type="application/json">"a"</script>')

from django.test import SimpleTestCase
from django.utils.functional import lazystr
from django.utils.html import json_script

class TestJsonScriptElementIdEdgeCases(SimpleTestCase):

    def test_empty_string_element_id_results_in_no_id_attribute(self):
        self.assertEqual(json_script('x', ''), '<script type="application/json">"x"</script>')

    def test_false_element_id_results_in_no_id_attribute(self):
        self.assertEqual(json_script('x', False), '<script type="application/json">"x"</script>')

    def test_zero_element_id_results_in_no_id_attribute(self):
        self.assertEqual(json_script('x', 0), '<script type="application/json">"x"</script>')

    def test_lazy_empty_string_element_id_results_in_no_id_attribute(self):
        self.assertEqual(json_script('x', lazystr('')), '<script type="application/json">"x"</script>')

from django.test import SimpleTestCase
from django.utils.html import json_script
from django.test import SimpleTestCase
from django.utils.html import json_script

class JsonScriptElementIdTests(SimpleTestCase):

    def test_empty_string_element_id_produces_no_id_attribute(self):
        result = json_script({'key': 'value'}, '')
        self.assertNotIn(' id="', result)
        self.assertIn('{"key": "value"}', result)

    def test_zero_int_element_id_produces_no_id_attribute(self):
        result = json_script('x', 0)
        self.assertNotIn(' id="', result)
        self.assertIn('"x"', result)

    def test_false_element_id_produces_no_id_attribute(self):
        result = json_script('x', False)
        self.assertNotIn(' id="', result)
        self.assertIn('"x"', result)

    def test_empty_bytes_element_id_produces_no_id_attribute(self):
        result = json_script('x', b'')
        self.assertNotIn(' id="', result)
        self.assertIn('"x"', result)

    def test_empty_string_element_id_with_escaped_content(self):
        result = json_script('&<>', '')
        self.assertNotIn(' id="', result)
        self.assertIn('\\u0026\\u003C\\u003E', result)

    def test_dict_value_escaped_and_no_id_for_empty_element(self):
        value = {'a': '<script>test&ing</script>'}
        result = json_script(value, '')
        self.assertNotIn(' id="', result)
        self.assertIn('\\u003Cscript\\u003Etest\\u0026ing\\u003C/script\\u003E', result)

    def test_false_element_id_with_complex_value_has_no_id_and_is_escaped(self):
        value = {'a': '<tag>&</tag>'}
        result = json_script(value, False)
        self.assertNotIn(' id="', result)
        self.assertIn('\\u003Ctag\\u003E\\u0026\\u003C/tag\\u003E', result)

from django.test import SimpleTestCase
from django.utils.functional import lazystr
from django.utils.html import json_script
from django.test import SimpleTestCase
from django.utils.functional import lazystr
from django.utils.html import json_script

class TestJsonScriptOptionalId(SimpleTestCase):

    def test_empty_string_id_omitted_for_string_value(self):
        self.assertEqual(json_script('&<>', ''), '<script type="application/json">"\\u0026\\u003C\\u003E"</script>')

    def test_empty_string_id_omitted_for_dict_value(self):
        self.assertEqual(json_script({'a': '<script>test&ing</script>'}, ''), '<script type="application/json">{"a": "\\u003Cscript\\u003Etest\\u0026ing\\u003C/script\\u003E"}</script>')

    def test_zero_id_is_omitted(self):
        self.assertEqual(json_script({'key': 'value'}, 0), '<script type="application/json">{"key": "value"}</script>')

    def test_false_id_is_omitted(self):
        self.assertEqual(json_script('abc', False), '<script type="application/json">"abc"</script>')

    def test_lazy_value_and_empty_id_omitted(self):
        self.assertEqual(json_script(lazystr('&<>'), ''), '<script type="application/json">"\\u0026\\u003C\\u003E"</script>')

    def test_large_content_and_empty_id_omitted(self):
        large = 'a' * 10000 + '<>&'
        expected = '<script type="application/json">"' + 'a' * 10000 + '\\u003C\\u003E\\u0026' + '"</script>'
        self.assertEqual(json_script(large, ''), expected)