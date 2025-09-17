#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.test_json_script_empty_id_equals_no_arg utils_tests.test_html_llm.test_json_script_empty_string_id_not_rendered utils_tests.test_html_llm.test_json_script_false_id_not_rendered utils_tests.test_html_llm.test_json_script_falsey_marked_safe_empty_equals_no_arg utils_tests.test_html_llm.test_json_script_id_escaping_angle_amp utils_tests.test_html_llm.test_json_script_id_escaping_quotes utils_tests.test_html_llm.test_json_script_lazy_empty_id_not_rendered utils_tests.test_html_llm.test_json_script_lazy_nonempty_id_rendered utils_tests.test_html_llm.test_json_script_mark_safe_empty_id_not_rendered utils_tests.test_html_llm.test_json_script_zero_id_not_rendered
coverage json -o coverage.json
: '>>>>> End Test Output'
