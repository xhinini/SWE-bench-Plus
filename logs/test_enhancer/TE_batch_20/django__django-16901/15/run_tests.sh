#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorRegressionTests._force_no_xor_feature xor_lookups.tests_llm.XorRegressionTests._restore_xor_feature xor_lookups.tests_llm.XorRegressionTests.setUpTestData xor_lookups.tests_llm.XorRegressionTests.test_associativity_of_chained_xor xor_lookups.tests_llm.XorRegressionTests.test_empty_in_with_multiple_xor xor_lookups.tests_llm.XorRegressionTests.test_exclude_with_multiple_xor xor_lookups.tests_llm.XorRegressionTests.test_many_children_xor xor_lookups.tests_llm.XorRegressionTests.test_mixed_negation_xor xor_lookups.tests_llm.XorRegressionTests.test_negated_entire_xor xor_lookups.tests_llm.XorRegressionTests.test_pk_xor_multiple xor_lookups.tests_llm.XorRegressionTests.test_three_way_xor_filter xor_lookups.tests_llm.XorRegressionTests.test_two_way_xor_filter xor_lookups.tests_llm.XorRegressionTests.test_values_list_flat_with_xor
coverage json -o coverage.json
: '>>>>> End Test Output'
