#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.CustomNonDBAttrsTests.test_alter_custom_binaryfield_non_db_attr_noop schema.tests_llm.CustomNonDBAttrsTests.test_alter_custom_charfield_non_db_attr_noop schema.tests_llm.CustomNonDBAttrsTests.test_alter_custom_charfield_non_db_attr_noop_none_to_value schema.tests_llm.CustomNonDBAttrsTests.test_alter_custom_integerfield_non_db_attr_noop schema.tests_llm.CustomNonDBAttrsTests.test_alter_custom_textfield_non_db_attr_noop schema.tests_llm.CustomNonDBAttrsTests.test_alter_only_new_field_has_non_db_attr_noop schema.tests_llm.CustomNonDBAttrsTests.test_alter_only_old_field_has_non_db_attr_noop schema.tests_llm.CustomNonDBAttrsTests.test_multiple_field_types_with_non_db_attr_ignored
coverage json -o coverage.json
: '>>>>> End Test Output'
