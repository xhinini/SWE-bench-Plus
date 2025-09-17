#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorLookupsTests.setUpTestData xor_lookups.tests_llm.XorLookupsTests.test_chain_mixed_q_and_qs xor_lookups.tests_llm.XorLookupsTests.test_empty_in xor_lookups.tests_llm.XorLookupsTests.test_exclude xor_lookups.tests_llm.XorLookupsTests.test_exclude_multiple_xor xor_lookups.tests_llm.XorLookupsTests.test_filter xor_lookups.tests_llm.XorLookupsTests.test_filter_multiple xor_lookups.tests_llm.XorLookupsTests.test_filter_negated xor_lookups.tests_llm.XorLookupsTests.test_five_way_xor_values_list xor_lookups.tests_llm.XorLookupsTests.test_four_way_xor_qs xor_lookups.tests_llm.XorLookupsTests.test_negated_chain_of_three_querysets xor_lookups.tests_llm.XorLookupsTests.test_pk_q xor_lookups.tests_llm.XorLookupsTests.test_stages xor_lookups.tests_llm.XorLookupsTests.test_three_way_xor_qs xor_lookups.tests_llm.XorLookupsTests.test_three_way_xor_with_negation xor_lookups.tests_llm.XorLookupsTests.test_xor_with_empty_queryset_in_chain
coverage json -o coverage.json
: '>>>>> End Test Output'
