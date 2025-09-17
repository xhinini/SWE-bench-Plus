#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.NonDBAttrsAlterFieldTests.test_alter_field_choices_noop_new_has_choices schema.tests_llm.NonDBAttrsAlterFieldTests.test_alter_field_db_column_noop_when_column_name_unchanged schema.tests_llm.NonDBAttrsAlterFieldTests.test_alter_field_editable_and_blank_noop schema.tests_llm.NonDBAttrsAlterFieldTests.test_alter_field_error_messages_noop schema.tests_llm.NonDBAttrsAlterFieldTests.test_alter_field_help_text_noop schema.tests_llm.NonDBAttrsAlterFieldTests.test_alter_field_limit_choices_to_noop_on_fk schema.tests_llm.NonDBAttrsAlterFieldTests.test_alter_field_on_delete_noop_on_fk schema.tests_llm.NonDBAttrsAlterFieldTests.test_alter_field_related_name_noop_on_fk schema.tests_llm.NonDBAttrsAlterFieldTests.test_alter_field_validators_noop schema.tests_llm.NonDBAttrsAlterFieldTests.test_alter_field_verbose_name_noop
coverage json -o coverage.json
: '>>>>> End Test Output'
