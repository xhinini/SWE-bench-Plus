#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_regression_alter_charfield_add_choices_noop schema.tests_llm.test_regression_alter_charfield_blank_editable_noop schema.tests_llm.test_regression_alter_charfield_change_validators_noop schema.tests_llm.test_regression_alter_charfield_choices_directional_noop schema.tests_llm.test_regression_alter_charfield_error_messages_noop schema.tests_llm.test_regression_alter_charfield_help_text_verbose_name_noop schema.tests_llm.test_regression_alter_charfield_limit_choices_to_noop schema.tests_llm.test_regression_alter_fk_many_non_db_attrs_combined_noop schema.tests_llm.test_regression_alter_fk_related_names_noop
coverage json -o coverage.json
: '>>>>> End Test Output'
