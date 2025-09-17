#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.test_json_script_empty_list_id utils_tests.test_html_llm.test_json_script_empty_string_id utils_tests.test_html_llm.test_json_script_escaped_id utils_tests.test_html_llm.test_json_script_false_id utils_tests.test_html_llm.test_json_script_integer_id utils_tests.test_html_llm.test_json_script_lazystr_id utils_tests.test_html_llm.test_json_script_mark_safe_id utils_tests.test_html_llm.test_json_script_space_id utils_tests.test_html_llm.test_json_script_string_zero_id utils_tests.test_html_llm.test_json_script_zero_id
coverage json -o coverage.json
: '>>>>> End Test Output'
