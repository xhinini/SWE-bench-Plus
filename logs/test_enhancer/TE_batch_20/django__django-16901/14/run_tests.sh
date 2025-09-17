#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorRegressionTests._expected_by_conditions xor_lookups.tests_llm.XorRegressionTests._force_no_xor_feature xor_lookups.tests_llm.XorRegressionTests.setUpTestData xor_lookups.tests_llm.XorRegressionTests.test_queryset_xor_operator_multiple xor_lookups.tests_llm.XorRegressionTests.test_xor_empty_in_multiple xor_lookups.tests_llm.XorRegressionTests.test_xor_exclude_multiple xor_lookups.tests_llm.XorRegressionTests.test_xor_five_filters_values_list xor_lookups.tests_llm.XorRegressionTests.test_xor_four_filters xor_lookups.tests_llm.XorRegressionTests.test_xor_negated_mixed xor_lookups.tests_llm.XorRegressionTests.test_xor_pk_q_multiple xor_lookups.tests_llm.XorRegressionTests.test_xor_stage_case xor_lookups.tests_llm.XorRegressionTests.test_xor_three_filters xor_lookups.tests_llm.XorRegressionTests.test_xor_with_and_or_combination
coverage json -o coverage.json
: '>>>>> End Test Output'
