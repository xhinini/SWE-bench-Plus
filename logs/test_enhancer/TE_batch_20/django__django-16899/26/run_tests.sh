#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_checks.tests_llm.test_missing_readonly_field_in_stacked_inline_includes_field_name admin_checks.tests_llm.test_missing_readonly_field_in_tabular_inline_includes_field_name admin_checks.tests_llm.test_missing_readonly_field_includes_field_name_index0 admin_checks.tests_llm.test_missing_readonly_field_includes_field_name_index1 admin_checks.tests_llm.test_missing_readonly_field_on_book_model_includes_field_name admin_checks.tests_llm.test_missing_readonly_field_on_inline_multiple_indices admin_checks.tests_llm.test_missing_readonly_field_with_custom_admin_class_name_reflected_in_message admin_checks.tests_llm.test_multiple_missing_readonly_fields_report_each_name admin_checks.tests_llm.test_two_missing_readonly_fields_order_and_names_preserved
coverage json -o coverage.json
: '>>>>> End Test Output'
