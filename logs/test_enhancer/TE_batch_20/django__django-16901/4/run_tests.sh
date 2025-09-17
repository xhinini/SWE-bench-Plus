#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.MultiOperandXorTests._expected_by_conds xor_lookups.tests_llm.MultiOperandXorTests.setUpTestData xor_lookups.tests_llm.MultiOperandXorTests.test_empty_in_multi_xor xor_lookups.tests_llm.MultiOperandXorTests.test_exclude_multi_xor xor_lookups.tests_llm.MultiOperandXorTests.test_four_way_q_xor xor_lookups.tests_llm.MultiOperandXorTests.test_negated_multi_xor xor_lookups.tests_llm.MultiOperandXorTests.test_nested_xor xor_lookups.tests_llm.MultiOperandXorTests.test_pk_multi_xor xor_lookups.tests_llm.MultiOperandXorTests.test_sql_compiles_for_multi_xor xor_lookups.tests_llm.MultiOperandXorTests.test_three_queryset_xor xor_lookups.tests_llm.MultiOperandXorTests.test_three_way_q_xor xor_lookups.tests_llm.MultiOperandXorTests.test_values_list_multi_xor
coverage json -o coverage.json
: '>>>>> End Test Output'
