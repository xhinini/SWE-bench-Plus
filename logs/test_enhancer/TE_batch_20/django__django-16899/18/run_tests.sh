#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_checks.tests_llm.test_readonly_nonexistent_field_classname_in_message admin_checks.tests_llm.test_readonly_nonexistent_field_index1_includes_field_name admin_checks.tests_llm.test_readonly_nonexistent_field_index9_includes_field_name admin_checks.tests_llm.test_readonly_nonexistent_field_inline_custom_classname_in_message admin_checks.tests_llm.test_readonly_nonexistent_field_inline_index0_includes_field_name admin_checks.tests_llm.test_readonly_nonexistent_field_model_label_in_message admin_checks.tests_llm.test_readonly_nonexistent_field_multiple_missing_reports_all admin_checks.tests_llm.test_readonly_nonexistent_field_special_chars_name_includes_field_name admin_checks.tests_llm.test_readonly_nonexistent_field_tuple_index0_includes_field_name
coverage json -o coverage.json
: '>>>>> End Test Output'
