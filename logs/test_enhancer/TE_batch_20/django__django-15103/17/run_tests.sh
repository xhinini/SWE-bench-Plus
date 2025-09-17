#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.JsonScriptFalsyIdTests._expected_no_id utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_json_script_custom_falsy_object_omits_id utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_json_script_empty_bytearray_omits_id utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_json_script_empty_bytes_omits_id utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_json_script_empty_dict_omits_id utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_json_script_empty_list_omits_id utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_json_script_empty_set_omits_id utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_json_script_empty_string_omits_id utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_json_script_empty_tuple_omits_id utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_json_script_false_omits_id utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_json_script_zero_omits_id
coverage json -o coverage.json
: '>>>>> End Test Output'
