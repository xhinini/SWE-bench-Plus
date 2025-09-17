#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorWhereNodeRegressionTests.setUpTestData xor_lookups.tests_llm.XorWhereNodeRegressionTests.test_chained_xor_and_other_lookups xor_lookups.tests_llm.XorWhereNodeRegressionTests.test_exclude_with_three_way_xor xor_lookups.tests_llm.XorWhereNodeRegressionTests.test_five_way_xor_filter xor_lookups.tests_llm.XorWhereNodeRegressionTests.test_four_way_xor_filter xor_lookups.tests_llm.XorWhereNodeRegressionTests.test_three_way_xor_filter xor_lookups.tests_llm.XorWhereNodeRegressionTests.test_three_way_xor_negated xor_lookups.tests_llm.XorWhereNodeRegressionTests.test_three_way_xor_sql_uses_mod xor_lookups.tests_llm.XorWhereNodeRegressionTests.test_two_way_xor_sql_does_not_use_mod xor_lookups.tests_llm.XorWhereNodeRegressionTests.test_xor_with_empty_in_and_three_operands
coverage json -o coverage.json
: '>>>>> End Test Output'
