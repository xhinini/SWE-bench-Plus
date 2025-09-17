#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_checks.tests_llm.test_callable_first_then_missing_field_index1 admin_checks.tests_llm.test_missing_readonly_field_message_includes_field_name_index0 admin_checks.tests_llm.test_missing_readonly_field_message_includes_field_name_index1 admin_checks.tests_llm.test_missing_readonly_field_model_label_includes_app_label admin_checks.tests_llm.test_missing_readonly_field_on_custom_admin_name admin_checks.tests_llm.test_missing_readonly_field_on_inline admin_checks.tests_llm.test_missing_readonly_field_with_special_characters_in_name admin_checks.tests_llm.test_multiple_missing_readonly_fields_on_inline_with_names_and_indices admin_checks.tests_llm.test_multiple_missing_readonly_fields_produce_two_errors
coverage json -o coverage.json
: '>>>>> End Test Output'
