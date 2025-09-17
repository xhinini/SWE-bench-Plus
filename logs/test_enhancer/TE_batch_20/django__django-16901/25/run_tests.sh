#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorLookupsTests.setUpTestData xor_lookups.tests_llm.XorLookupsTests.test_empty_in_three_way xor_lookups.tests_llm.XorLookupsTests.test_exclude_three_way xor_lookups.tests_llm.XorLookupsTests.test_filter_five_way_consistency xor_lookups.tests_llm.XorLookupsTests.test_filter_four_way_mod_needed xor_lookups.tests_llm.XorLookupsTests.test_filter_three_way_mod_needed xor_lookups.tests_llm.XorLookupsTests.test_filter_three_way_negated_mod_needed xor_lookups.tests_llm.XorLookupsTests.test_pk_q_three_way xor_lookups.tests_llm.XorLookupsTests.test_querysets_chain_three_way xor_lookups.tests_llm.XorLookupsTests.test_values_list_three_way
coverage json -o coverage.json
: '>>>>> End Test Output'
