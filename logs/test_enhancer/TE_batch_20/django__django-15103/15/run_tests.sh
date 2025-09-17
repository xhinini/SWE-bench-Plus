#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.test_json_script_empty_string_id_absent utils_tests.test_html_llm.test_json_script_empty_value_and_empty_id_absent utils_tests.test_html_llm.test_json_script_false_id_absent utils_tests.test_html_llm.test_json_script_mark_safe_empty_id_absent utils_tests.test_html_llm.test_json_script_mark_safe_nonempty_id_rendered utils_tests.test_html_llm.test_json_script_none_id_absent utils_tests.test_html_llm.test_json_script_special_chars_escaped_and_no_id_for_empty utils_tests.test_html_llm.test_json_script_with_lazystr_id_present utils_tests.test_html_llm.test_json_script_with_string_id_present utils_tests.test_html_llm.test_json_script_zero_id_absent
coverage json -o coverage.json
: '>>>>> End Test Output'
