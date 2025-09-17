#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.TestJsonScriptFalsyIds.setUp utils_tests.test_html_llm.TestJsonScriptFalsyIds.test_json_script_empty_bytearray_id_ignored utils_tests.test_html_llm.TestJsonScriptFalsyIds.test_json_script_empty_bytes_id_ignored utils_tests.test_html_llm.TestJsonScriptFalsyIds.test_json_script_empty_dict_id_ignored utils_tests.test_html_llm.TestJsonScriptFalsyIds.test_json_script_empty_list_id_ignored utils_tests.test_html_llm.TestJsonScriptFalsyIds.test_json_script_empty_set_id_ignored utils_tests.test_html_llm.TestJsonScriptFalsyIds.test_json_script_empty_string_id_ignored utils_tests.test_html_llm.TestJsonScriptFalsyIds.test_json_script_empty_tuple_id_ignored utils_tests.test_html_llm.TestJsonScriptFalsyIds.test_json_script_false_id_ignored utils_tests.test_html_llm.TestJsonScriptFalsyIds.test_json_script_zero_id_ignored
coverage json -o coverage.json
: '>>>>> End Test Output'
