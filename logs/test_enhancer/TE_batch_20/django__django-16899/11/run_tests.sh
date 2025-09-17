#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_checks.tests_llm.test_missing_readonly_field_at_higher_index admin_checks.tests_llm.test_missing_readonly_field_includes_field_name_modeladmin admin_checks.tests_llm.test_missing_readonly_field_includes_field_name_tabularinline admin_checks.tests_llm.test_missing_readonly_field_message_includes_admin_class_name admin_checks.tests_llm.test_missing_readonly_field_message_includes_model_label admin_checks.tests_llm.test_missing_readonly_field_on_inline_class_with_custom_name admin_checks.tests_llm.test_missing_readonly_fields_with_similar_names_do_not_confuse_labels admin_checks.tests_llm.test_multiple_missing_readonly_fields_have_correct_labels_and_field_names admin_checks.tests_llm.test_multiple_missing_readonly_fields_order_and_labels_for_inline
coverage json -o coverage.json
: '>>>>> End Test Output'
