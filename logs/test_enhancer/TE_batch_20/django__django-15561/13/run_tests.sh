#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.NonDbAttrsRegressionTests.test_alter_charfield_add_choices_noop schema.tests_llm.NonDbAttrsRegressionTests.test_alter_charfield_error_messages_noop schema.tests_llm.NonDbAttrsRegressionTests.test_alter_charfield_help_text_noop schema.tests_llm.NonDbAttrsRegressionTests.test_alter_charfield_limit_choices_to_noop schema.tests_llm.NonDbAttrsRegressionTests.test_alter_charfield_validators_noop schema.tests_llm.NonDbAttrsRegressionTests.test_alter_charfield_verbose_name_and_choices_combined_noop schema.tests_llm.NonDbAttrsRegressionTests.test_alter_charfield_verbose_name_noop schema.tests_llm.NonDbAttrsRegressionTests.test_alter_foreignkey_on_delete_noop schema.tests_llm.NonDbAttrsRegressionTests.test_alter_foreignkey_related_name_noop schema.tests_llm.NonDbAttrsRegressionTests.test_alter_foreignkey_related_query_name_noop
coverage json -o coverage.json
: '>>>>> End Test Output'
