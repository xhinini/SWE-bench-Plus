#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.AddNullableFieldTests._run_add_field_and_assert_nullable schema.tests_llm.AddNullableFieldTests.setUp schema.tests_llm.AddNullableFieldTests.tearDown schema.tests_llm.AddNullableFieldTests.test_add_nullable_binaryfield schema.tests_llm.AddNullableFieldTests.test_add_nullable_booleanfield schema.tests_llm.AddNullableFieldTests.test_add_nullable_charfield schema.tests_llm.AddNullableFieldTests.test_add_nullable_datefield schema.tests_llm.AddNullableFieldTests.test_add_nullable_datetimefield schema.tests_llm.AddNullableFieldTests.test_add_nullable_decimalfield schema.tests_llm.AddNullableFieldTests.test_add_nullable_durationfield schema.tests_llm.AddNullableFieldTests.test_add_nullable_integerfield schema.tests_llm.AddNullableFieldTests.test_add_nullable_textfield schema.tests_llm.AddNullableFieldTests.test_add_nullable_timefield
coverage json -o coverage.json
: '>>>>> End Test Output'
