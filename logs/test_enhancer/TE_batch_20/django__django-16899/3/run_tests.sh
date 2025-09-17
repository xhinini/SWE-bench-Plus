#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_checks.tests_llm.test_readonly_missing_field_index_one admin_checks.tests_llm.test_readonly_missing_field_index_zero admin_checks.tests_llm.test_readonly_missing_field_inherited_admin_name_in_message admin_checks.tests_llm.test_readonly_missing_field_label_and_fieldname_with_special_chars admin_checks.tests_llm.test_readonly_missing_field_multiple_on_modeladmin admin_checks.tests_llm.test_readonly_missing_field_on_custom_named_admin admin_checks.tests_llm.test_readonly_missing_field_on_inline_index_two admin_checks.tests_llm.test_readonly_missing_field_on_stacked_inline_shows_inline_class_name admin_checks.tests_llm.test_readonly_missing_field_on_tabular_inline_shows_inline_class_name
coverage json -o coverage.json
: '>>>>> End Test Output'
