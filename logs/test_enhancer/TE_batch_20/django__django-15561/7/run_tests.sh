#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_alter_charfield_choices_noop_extra schema.tests_llm.test_alter_field_add_non_db_attr_on_new_field_noop schema.tests_llm.test_alter_field_blank_only_noop schema.tests_llm.test_alter_field_editable_noop schema.tests_llm.test_alter_field_error_messages_noop schema.tests_llm.test_alter_field_help_text_noop_extra schema.tests_llm.test_alter_field_limit_choices_to_noop schema.tests_llm.test_alter_field_related_name_noop schema.tests_llm.test_alter_field_validators_noop schema.tests_llm.test_alter_field_verbose_name_noop
coverage json -o coverage.json
: '>>>>> End Test Output'
