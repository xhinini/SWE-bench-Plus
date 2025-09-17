#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.JsonScriptFalseyElementIdTests.setUp utils_tests.test_html_llm.JsonScriptFalseyElementIdTests.test_empty_bytearray_omits_id utils_tests.test_html_llm.JsonScriptFalseyElementIdTests.test_empty_dict_omits_id utils_tests.test_html_llm.JsonScriptFalseyElementIdTests.test_empty_frozenset_omits_id utils_tests.test_html_llm.JsonScriptFalseyElementIdTests.test_empty_list_omits_id utils_tests.test_html_llm.JsonScriptFalseyElementIdTests.test_empty_range_omits_id utils_tests.test_html_llm.JsonScriptFalseyElementIdTests.test_empty_string_omits_id utils_tests.test_html_llm.JsonScriptFalseyElementIdTests.test_empty_tuple_omits_id utils_tests.test_html_llm.JsonScriptFalseyElementIdTests.test_false_boolean_omits_id utils_tests.test_html_llm.JsonScriptFalseyElementIdTests.test_zero_float_omits_id utils_tests.test_html_llm.JsonScriptFalseyElementIdTests.test_zero_integer_omits_id
coverage json -o coverage.json
: '>>>>> End Test Output'
