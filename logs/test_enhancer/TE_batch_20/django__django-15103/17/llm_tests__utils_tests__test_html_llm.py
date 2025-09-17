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

def test_json_script_falsy_element_ids_are_treated_as_no_id(self):
    value = {'key': 'value'}
    expected = '<script type="application/json">{"key": "value"}</script>'
    falsy_ids = ['', False, 0, 0.0, [], (), set(), frozenset(), lazystr(''), mark_safe('')]
    for eid in falsy_ids:
        with self.subTest(element_id=repr(eid)):
            self.assertEqual(json_script(value, eid), expected)

from django.test import SimpleTestCase
from django.utils.functional import lazystr
from django.utils.html import json_script


class JsonScriptElementIdTests(SimpleTestCase):
    def test_empty_string_element_id_with_simple_string(self):
        result = json_script("x", "")
        self.assertEqual(result, '<script type="application/json">"x"</script>')

    def test_empty_string_element_id_with_dict(self):
        result = json_script({"a": "b"}, "")
        self.assertEqual(result, '<script type="application/json">{"a": "b"}</script>')

    def test_empty_string_element_id_with_lazy_string(self):
        result = json_script(lazystr("x"), "")
        self.assertEqual(result, '<script type="application/json">"x"</script>')

    def test_empty_string_element_id_with_nested_lazy(self):
        # Ensure escaping still occurs and no id attribute is present.
        result = json_script({"a": lazystr("<&>")}, "")
        self.assertEqual(
            result,
            '<script type="application/json">{"a": "\\u003C\\u0026\\u003E"}</script>'
        )

    def test_zero_element_id_with_simple_string(self):
        # element_id=0 should be treated like "not provided" and NOT render id="0"
        result = json_script("x", 0)
        self.assertEqual(result, '<script type="application/json">"x"</script>')

    def test_zero_element_id_with_dict(self):
        result = json_script({"a": "b"}, 0)
        self.assertEqual(result, '<script type="application/json">{"a": "b"}</script>')

    def test_zero_element_id_with_lazy_string(self):
        result = json_script(lazystr("x"), 0)
        self.assertEqual(result, '<script type="application/json">"x"</script>')

    def test_zero_element_id_with_nested_lazy(self):
        result = json_script({"a": lazystr("<&>")}, 0)
        self.assertEqual(
            result,
            '<script type="application/json">{"a": "\\u003C\\u0026\\u003E"}</script>'
        )

    def test_false_element_id_is_treated_as_no_id(self):
        # False should not produce an id attribute.
        result = json_script("x", False)
        self.assertEqual(result, '<script type="application/json">"x"</script>')

    def test_empty_list_element_id_is_treated_as_no_id(self):
        # An empty list (falsy) should not produce an id attribute.
        result = json_script({"a": "b"}, [])
        self.assertEqual(result, '<script type="application/json">{"a": "b"}</script>')

from django.utils.functional import lazystr
from django.test import SimpleTestCase
from django.utils.functional import lazystr
from django.utils.html import json_script

class JsonScriptFalsyElementIdTests(SimpleTestCase):
    expected = '<script type="application/json">{"key": "value"}</script>'

    def test_empty_string_omits_id(self):
        self.check_omits_id('')

    def test_zero_int_omits_id(self):
        self.check_omits_id(0)

    def test_false_bool_omits_id(self):
        self.check_omits_id(False)

    def test_empty_list_omits_id(self):
        self.check_omits_id([])

    def test_empty_tuple_omits_id(self):
        self.check_omits_id(())

    def test_empty_dict_omits_id(self):
        self.check_omits_id({})

    def test_lazy_empty_string_omits_id(self):
        self.check_omits_id(lazystr(''))

    def test_empty_bytes_omits_id(self):
        self.check_omits_id(b'')

    def test_empty_bytearray_omits_id(self):
        self.check_omits_id(bytearray(b''))

    def test_empty_set_omits_id(self):
        self.check_omits_id(set())

from django.test import SimpleTestCase
from django.utils.functional import lazystr
from django.utils.html import json_script
from django.utils.safestring import mark_safe

class JsonScriptElementIdRegressionTests(SimpleTestCase):

    def test_empty_string_element_id_with_simple_string_value(self):
        result = json_script('x', '')
        self.assertEqual(result, '<script type="application/json">"x"</script>')

    def test_empty_string_element_id_with_special_chars_dict(self):
        result = json_script({'a': '<&>'}, '')
        self.assertEqual(result, '<script type="application/json">{"a": "\\u003C\\u0026\\u003E"}</script>')

    def test_zero_element_id_with_simple_string_value(self):
        result = json_script('x', 0)
        self.assertEqual(result, '<script type="application/json">"x"</script>')

    def test_zero_element_id_with_special_chars_dict(self):
        result = json_script({'a': '<&>'}, 0)
        self.assertEqual(result, '<script type="application/json">{"a": "\\u003C\\u0026\\u003E"}</script>')

    def test_false_element_id_with_simple_string_value(self):
        result = json_script('x', False)
        self.assertEqual(result, '<script type="application/json">"x"</script>')

    def test_false_element_id_with_special_chars_dict(self):
        result = json_script({'a': '<&>'}, False)
        self.assertEqual(result, '<script type="application/json">{"a": "\\u003C\\u0026\\u003E"}</script>')

    def test_mark_safe_empty_string_element_id_with_simple_string_value(self):
        result = json_script('x', mark_safe(''))
        self.assertEqual(result, '<script type="application/json">"x"</script>')

    def test_mark_safe_empty_string_element_id_with_special_chars_dict(self):
        result = json_script({'a': '<&>'}, mark_safe(''))
        self.assertEqual(result, '<script type="application/json">{"a": "\\u003C\\u0026\\u003E"}</script>')

from django.test import SimpleTestCase
from django.utils.functional import lazystr
from django.utils.html import json_script

class JsonScriptElementIdTests(SimpleTestCase):

    def test_empty_string_element_id_is_omitted(self):
        value = {'key': 'value'}
        without_id = json_script(value)
        with_empty = json_script(value, '')
        self.assertEqual(with_empty, without_id)

    def test_int_zero_element_id_is_omitted(self):
        value = {'key': 'value'}
        without_id = json_script(value)
        with_zero = json_script(value, 0)
        self.assertEqual(with_zero, without_id)

    def test_false_element_id_is_omitted(self):
        value = {'key': 'value'}
        without_id = json_script(value)
        with_false = json_script(value, False)
        self.assertEqual(with_false, without_id)

def test_json_script_empty_string_element_id_omitted(self):
    output = json_script('&<>', '')
    self.assertTrue(output.startswith('<script type="application/json">'))
    self.assertNotIn(' id=', output)
    self.assertIn('\\u0026\\u003C\\u003E', output)

def test_json_script_false_element_id_omitted(self):
    output = json_script('&<>', False)
    self.assertTrue(output.startswith('<script type="application/json">'))
    self.assertNotIn(' id=', output)
    self.assertIn('\\u0026\\u003C\\u003E', output)

def test_json_script_zero_element_id_omitted(self):
    output = json_script('&<>', 0)
    self.assertTrue(output.startswith('<script type="application/json">'))
    self.assertNotIn(' id=', output)
    self.assertIn('\\u0026\\u003C\\u003E', output)

def test_json_script_empty_list_element_id_omitted(self):
    output = json_script('&<>', [])
    self.assertTrue(output.startswith('<script type="application/json">'))
    self.assertNotIn(' id=', output)
    self.assertIn('\\u0026\\u003C\\u003E', output)

def test_json_script_empty_tuple_element_id_omitted(self):
    output = json_script('&<>', ())
    self.assertTrue(output.startswith('<script type="application/json">'))
    self.assertNotIn(' id=', output)
    self.assertIn('\\u0026\\u003C\\u003E', output)

def test_json_script_empty_dict_element_id_omitted(self):
    output = json_script('&<>', {})
    self.assertTrue(output.startswith('<script type="application/json">'))
    self.assertNotIn(' id=', output)
    self.assertIn('\\u0026\\u003C\\u003E', output)

def test_json_script_empty_bytes_element_id_omitted(self):
    output = json_script('&<>', b'')
    self.assertTrue(output.startswith('<script type="application/json">'))
    self.assertNotIn(' id=', output)
    self.assertIn('\\u0026\\u003C\\u003E', output)

def test_json_script_empty_bytearray_element_id_omitted(self):
    output = json_script('&<>', bytearray(b''))
    self.assertTrue(output.startswith('<script type="application/json">'))
    self.assertNotIn(' id=', output)
    self.assertIn('\\u0026\\u003C\\u003E', output)

def test_json_script_zero_float_element_id_omitted(self):
    output = json_script('&<>', 0.0)
    self.assertTrue(output.startswith('<script type="application/json">'))
    self.assertNotIn(' id=', output)
    self.assertIn('\\u0026\\u003C\\u003E', output)

def test_json_script_empty_range_element_id_omitted(self):
    output = json_script('&<>', range(0))
    self.assertTrue(output.startswith('<script type="application/json">'))
    self.assertNotIn(' id=', output)
    self.assertIn('\\u0026\\u003C\\u003E', output)

from django.test import SimpleTestCase
from django.utils.html import json_script
from django.test import SimpleTestCase
from django.utils.html import json_script

class TestJsonScriptFalsyIds(SimpleTestCase):

    def setUp(self):
        self.payload = {'key': 'value'}

    def test_json_script_empty_string_id_ignored(self):
        self.assertEqual(json_script(self.payload, ''), json_script(self.payload))

    def test_json_script_false_id_ignored(self):
        self.assertEqual(json_script(self.payload, False), json_script(self.payload))

    def test_json_script_zero_id_ignored(self):
        self.assertEqual(json_script(self.payload, 0), json_script(self.payload))

    def test_json_script_empty_list_id_ignored(self):
        self.assertEqual(json_script(self.payload, []), json_script(self.payload))

    def test_json_script_empty_tuple_id_ignored(self):
        self.assertEqual(json_script(self.payload, ()), json_script(self.payload))

    def test_json_script_empty_dict_id_ignored(self):
        self.assertEqual(json_script(self.payload, {}), json_script(self.payload))

    def test_json_script_empty_bytes_id_ignored(self):
        self.assertEqual(json_script(self.payload, b''), json_script(self.payload))

    def test_json_script_empty_bytearray_id_ignored(self):
        self.assertEqual(json_script(self.payload, bytearray(b'')), json_script(self.payload))

    def test_json_script_empty_set_id_ignored(self):
        self.assertEqual(json_script(self.payload, set()), json_script(self.payload))

from django.test import SimpleTestCase
from django.utils.functional import lazystr
from django.utils.html import json_script
from django.test import SimpleTestCase
from django.utils.functional import lazystr
from django.utils.html import json_script

class JsonScriptFalsyIdTests(SimpleTestCase):

    def test_empty_string_id_results_in_no_id_attribute(self):
        output = json_script({'key': 'value'}, '')
        self.assertEqual(output, '<script type="application/json">{"key": "value"}</script>')

    def test_false_id_results_in_no_id_attribute(self):
        output = json_script({'key': 'value'}, False)
        self.assertEqual(output, '<script type="application/json">{"key": "value"}</script>')

    def test_zero_id_results_in_no_id_attribute(self):
        output = json_script({'key': 'value'}, 0)
        self.assertEqual(output, '<script type="application/json">{"key": "value"}</script>')

    def test_lazy_empty_string_id_results_in_no_id_attribute(self):
        output = json_script({'key': 'value'}, lazystr(''))
        self.assertEqual(output, '<script type="application/json">{"key": "value"}</script>')

    def test_empty_bytes_id_results_in_no_id_attribute(self):
        output = json_script({'key': 'value'}, b'')
        self.assertEqual(output, '<script type="application/json">{"key": "value"}</script>')

    def test_empty_list_id_results_in_no_id_attribute(self):
        output = json_script({'key': 'value'}, [])
        self.assertEqual(output, '<script type="application/json">{"key": "value"}</script>')

    def test_escaping_preserved_when_no_id(self):
        output = json_script('&<>', '')
        self.assertEqual(output, '<script type="application/json">"\\u0026\\u003C\\u003E"</script>')

from django.test import SimpleTestCase
from django.utils.functional import lazystr
from django.utils.safestring import mark_safe
from django.utils.html import json_script

class TestJsonScriptFalsyIDs(SimpleTestCase):

    def test_empty_string_id_omitted_for_dict(self):
        self.assertEqual(json_script({'key': 'value'}, element_id=''), '<script type="application/json">{"key": "value"}</script>')

    def test_empty_string_id_omitted_for_empty_value(self):
        self.assertEqual(json_script('', element_id=''), '<script type="application/json">""</script>')

    def test_lazy_empty_string_id_omitted(self):
        self.assertEqual(json_script({'key': 'value'}, element_id=lazystr('')), '<script type="application/json">{"key": "value"}</script>')

    def test_mark_safe_empty_string_id_omitted(self):
        self.assertEqual(json_script({'key': 'value'}, element_id=mark_safe('')), '<script type="application/json">{"key": "value"}</script>')

    def test_false_id_omitted(self):
        self.assertEqual(json_script({'key': 'value'}, element_id=False), '<script type="application/json">{"key": "value"}</script>')

    def test_zero_id_omitted(self):
        self.assertEqual(json_script({'key': 'value'}, element_id=0), '<script type="application/json">{"key": "value"}</script>')

    def test_lazy_value_with_empty_id_omitted(self):
        self.assertEqual(json_script(lazystr('x'), element_id=''), '<script type="application/json">"x"</script>')

    def test_mark_safe_value_and_empty_id_omitted(self):
        self.assertEqual(json_script(mark_safe('safe'), element_id=''), '<script type="application/json">"safe"</script>')

def test_json_script_empty_string_id_absent(self):
    result = json_script({'key': 'value'}, '')
    self.assertNotIn(' id="', result)
    self.assertIn('<script type="application/json">', result)
    self.assertIn('{"key": "value"}', result)

def test_json_script_mark_safe_empty_id_absent(self):
    result = json_script({'key': 'value'}, mark_safe(''))
    self.assertNotIn(' id="', result)
    self.assertIn('<script type="application/json">', result)
    self.assertIn('{"key": "value"}', result)

def test_json_script_zero_id_absent(self):
    result = json_script('x', 0)
    self.assertNotIn(' id="', result)
    self.assertIn('<script type="application/json">', result)
    self.assertIn('"x"', result)

def test_json_script_false_id_absent(self):
    result = json_script('x', False)
    self.assertNotIn(' id="', result)
    self.assertIn('<script type="application/json">', result)
    self.assertIn('"x"', result)

def test_json_script_none_id_absent(self):
    result = json_script('x', None)
    self.assertNotIn(' id="', result)
    self.assertIn('<script type="application/json">', result)
    self.assertIn('"x"', result)

def test_json_script_with_string_id_present(self):
    result = json_script('x', 'my-id')
    self.assertIn(' id="my-id"', result)
    self.assertIn('<script id="my-id" type="application/json">', result)
    self.assertIn('"x"', result)

def test_json_script_with_lazystr_id_present(self):
    lazy_id = lazystr('lazy-id')
    result = json_script('y', lazy_id)
    self.assertIn(' id="lazy-id"', result)
    self.assertIn('<script id="lazy-id" type="application/json">', result)
    self.assertIn('"y"', result)

def test_json_script_empty_value_and_empty_id_absent(self):
    result = json_script('', '')
    self.assertNotIn(' id="', result)
    self.assertIn('<script type="application/json">', result)
    self.assertIn('""', result)

def test_json_script_special_chars_escaped_and_no_id_for_empty(self):
    result = json_script('<&>', '')
    self.assertNotIn(' id="', result)
    self.assertIn('<script type="application/json">', result)
    self.assertIn('\\u003C', result)
    self.assertIn('\\u0026', result)
    self.assertIn('\\u003E', result)

def test_json_script_mark_safe_nonempty_id_rendered(self):
    safe_id = mark_safe('safe-id')
    result = json_script({'a': 1}, safe_id)
    self.assertIn(' id="safe-id"', result)
    self.assertIn('<script id="safe-id" type="application/json">', result)
    self.assertIn('{"a": 1}', result)

from django.utils.functional import lazystr
from django.utils.safestring import mark_safe
from django.test import SimpleTestCase
from django.utils.functional import lazystr
from django.utils.safestring import mark_safe
from django.utils.html import json_script

class JsonScriptElementIdTests(SimpleTestCase):

    def test_json_script_empty_string_id(self):
        self.assertEqual(json_script('abc', ''), '<script type="application/json">"abc"</script>')

    def test_json_script_false_id(self):
        self.assertEqual(json_script('abc', False), '<script type="application/json">"abc"</script>')

    def test_json_script_zero_id(self):
        self.assertEqual(json_script('abc', 0), '<script type="application/json">"abc"</script>')

    def test_json_script_lazy_empty_string_id(self):
        self.assertEqual(json_script('abc', lazystr('')), '<script type="application/json">"abc"</script>')

    def test_json_script_mark_safe_empty_id(self):
        self.assertEqual(json_script('abc', mark_safe('')), '<script type="application/json">"abc"</script>')

# No new imports required beyond what's in the test module (django.test.SimpleTestCase and django.utils.html.json_script).
from django.test import SimpleTestCase
from django.utils.html import json_script

class JsonScriptFalsyIdTests(SimpleTestCase):
    def _expected_no_id(self):
        return '<script type="application/json">{"key": "value"}</script>'

    def test_json_script_empty_string_omits_id(self):
        self.assertHTMLEqual(json_script({'key': 'value'}, ''), self._expected_no_id())

    def test_json_script_zero_omits_id(self):
        # 0 is falsy; should be treated as "no id"
        self.assertHTMLEqual(json_script({'key': 'value'}, 0), self._expected_no_id())

    def test_json_script_false_omits_id(self):
        # False is falsy; should be treated as "no id"
        self.assertHTMLEqual(json_script({'key': 'value'}, False), self._expected_no_id())

    def test_json_script_empty_list_omits_id(self):
        self.assertHTMLEqual(json_script({'key': 'value'}, []), self._expected_no_id())

    def test_json_script_empty_tuple_omits_id(self):
        self.assertHTMLEqual(json_script({'key': 'value'}, ()), self._expected_no_id())

    def test_json_script_empty_dict_omits_id(self):
        self.assertHTMLEqual(json_script({'key': 'value'}, {}), self._expected_no_id())

    def test_json_script_empty_bytes_omits_id(self):
        self.assertHTMLEqual(json_script({'key': 'value'}, b''), self._expected_no_id())

    def test_json_script_empty_set_omits_id(self):
        self.assertHTMLEqual(json_script({'key': 'value'}, set()), self._expected_no_id())

    def test_json_script_empty_bytearray_omits_id(self):
        self.assertHTMLEqual(json_script({'key': 'value'}, bytearray(b'')), self._expected_no_id())

    def test_json_script_custom_falsy_object_omits_id(self):
        class FalsyButNotNone:
            def __bool__(self):
                return False
            def __str__(self):
                return 'falsy'

        obj = FalsyButNotNone()
        # Object is not None, but is falsy via __bool__; should be treated as "no id"
        self.assertHTMLEqual(json_script({'key': 'value'}, obj), self._expected_no_id())