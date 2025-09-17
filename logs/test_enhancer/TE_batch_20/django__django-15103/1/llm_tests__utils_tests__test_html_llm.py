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