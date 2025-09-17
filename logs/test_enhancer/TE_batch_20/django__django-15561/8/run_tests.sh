#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.SchemaNonDBAttrsTests._assert_field_should_not_be_altered schema.tests_llm.SchemaNonDBAttrsTests.test_ignore_custom_non_db_attr_only_new_class_10 schema.tests_llm.SchemaNonDBAttrsTests.test_ignore_custom_non_db_attr_only_new_class_6 schema.tests_llm.SchemaNonDBAttrsTests.test_ignore_custom_non_db_attr_only_new_class_7 schema.tests_llm.SchemaNonDBAttrsTests.test_ignore_custom_non_db_attr_only_new_class_8 schema.tests_llm.SchemaNonDBAttrsTests.test_ignore_custom_non_db_attr_only_new_class_9 schema.tests_llm.SchemaNonDBAttrsTests.test_ignore_custom_non_db_attr_same_class_1 schema.tests_llm.SchemaNonDBAttrsTests.test_ignore_custom_non_db_attr_same_class_2 schema.tests_llm.SchemaNonDBAttrsTests.test_ignore_custom_non_db_attr_same_class_3 schema.tests_llm.SchemaNonDBAttrsTests.test_ignore_custom_non_db_attr_same_class_4 schema.tests_llm.SchemaNonDBAttrsTests.test_ignore_custom_non_db_attr_same_class_5
coverage json -o coverage.json
: '>>>>> End Test Output'
