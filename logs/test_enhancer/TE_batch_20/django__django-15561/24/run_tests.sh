#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.NonDBAttrAlterationTests._run_noop_alter_test schema.tests_llm.NonDBAttrAlterationTests.test_binaryfield_custom_non_db_attr_noop schema.tests_llm.NonDBAttrAlterationTests.test_booleanfield_custom_non_db_attr_noop schema.tests_llm.NonDBAttrAlterationTests.test_charfield_custom_non_db_attr_noop schema.tests_llm.NonDBAttrAlterationTests.test_datefield_custom_non_db_attr_noop schema.tests_llm.NonDBAttrAlterationTests.test_decimalfield_custom_non_db_attr_noop schema.tests_llm.NonDBAttrAlterationTests.test_durationfield_custom_non_db_attr_noop schema.tests_llm.NonDBAttrAlterationTests.test_floatfield_custom_non_db_attr_noop schema.tests_llm.NonDBAttrAlterationTests.test_integerfield_custom_non_db_attr_noop schema.tests_llm.NonDBAttrAlterationTests.test_timefield_custom_non_db_attr_noop schema.tests_llm.NonDBAttrAlterationTests.test_uuidfield_custom_non_db_attr_noop
coverage json -o coverage.json
: '>>>>> End Test Output'
