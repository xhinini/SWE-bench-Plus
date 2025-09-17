#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorLookupsTests.setUpTestData xor_lookups.tests_llm.XorLookupsTests.test_empty_in xor_lookups.tests_llm.XorLookupsTests.test_empty_in_combination_multiple_xor xor_lookups.tests_llm.XorLookupsTests.test_even_parity_matches_expected xor_lookups.tests_llm.XorLookupsTests.test_exclude xor_lookups.tests_llm.XorLookupsTests.test_filter xor_lookups.tests_llm.XorLookupsTests.test_filter_multiple xor_lookups.tests_llm.XorLookupsTests.test_filter_negated xor_lookups.tests_llm.XorLookupsTests.test_negated_three_way_xor xor_lookups.tests_llm.XorLookupsTests.test_pk_multiple_xor xor_lookups.tests_llm.XorLookupsTests.test_pk_q xor_lookups.tests_llm.XorLookupsTests.test_sql_contains_mod_when_converted xor_lookups.tests_llm.XorLookupsTests.test_stages xor_lookups.tests_llm.XorLookupsTests.test_three_way_xor_no_db_xor_flag xor_lookups.tests_llm.XorLookupsTests.test_three_way_xor_results xor_lookups.tests_llm.XorLookupsTests.test_two_way_xor_sym_diff xor_lookups.tests_llm.XorLookupsTests.test_values_list_multiple_xor
coverage json -o coverage.json
: '>>>>> End Test Output'
