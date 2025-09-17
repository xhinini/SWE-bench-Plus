#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_alter_field_choices_noop_regression schema.tests_llm.test_alter_field_error_messages_noop schema.tests_llm.test_alter_field_help_text_noop schema.tests_llm.test_alter_field_validators_noop schema.tests_llm.test_alter_field_verbose_name_and_help_text_combined_noop schema.tests_llm.test_alter_field_verbose_name_noop schema.tests_llm.test_alter_fk_editable_and_limit_choices_to_noop schema.tests_llm.test_alter_fk_on_delete_related_name_noop schema.tests_llm.test_alter_fk_related_query_name_noop
coverage json -o coverage.json
: '>>>>> End Test Output'
