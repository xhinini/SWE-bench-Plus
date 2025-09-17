#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.TestJsonScriptOptionalId.test_empty_bytes_id_is_treated_as_no_id utils_tests.test_html_llm.TestJsonScriptOptionalId.test_empty_list_id_is_treated_as_no_id utils_tests.test_html_llm.TestJsonScriptOptionalId.test_empty_string_id_is_treated_as_no_id utils_tests.test_html_llm.TestJsonScriptOptionalId.test_false_id_is_treated_as_no_id utils_tests.test_html_llm.TestJsonScriptOptionalId.test_lazy_empty_string_is_treated_as_no_id utils_tests.test_html_llm.TestJsonScriptOptionalId.test_object_with_false_bool_is_treated_as_no_id utils_tests.test_html_llm.TestJsonScriptOptionalId.test_zero_int_id_is_treated_as_no_id
coverage json -o coverage.json
: '>>>>> End Test Output'
