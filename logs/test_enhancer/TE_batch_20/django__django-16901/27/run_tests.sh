#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorLookupsTests._expected_by_thresholds xor_lookups.tests_llm.XorLookupsTests.setUpTestData xor_lookups.tests_llm.XorLookupsTests.test_empty_in_combined_with_many_xor xor_lookups.tests_llm.XorLookupsTests.test_exclude_multiple_xor_results xor_lookups.tests_llm.XorLookupsTests.test_five_way_xor_results_values_list xor_lookups.tests_llm.XorLookupsTests.test_four_way_xor_results xor_lookups.tests_llm.XorLookupsTests.test_mixed_q_and_queryset_xor xor_lookups.tests_llm.XorLookupsTests.test_negated_multiple_xor_results xor_lookups.tests_llm.XorLookupsTests.test_six_way_xor_queryset_chain xor_lookups.tests_llm.XorLookupsTests.test_three_way_xor_results xor_lookups.tests_llm.XorLookupsTests.test_where_as_sql_no_error_three_plus xor_lookups.tests_llm.XorLookupsTests.test_xor_with_pk_multiple
coverage json -o coverage.json
: '>>>>> End Test Output'
