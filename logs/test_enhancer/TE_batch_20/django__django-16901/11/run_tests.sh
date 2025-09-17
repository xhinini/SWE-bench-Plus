#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorLookupsTests.setUpTestData xor_lookups.tests_llm.XorLookupsTests.test_xor_five_children_values_list xor_lookups.tests_llm.XorLookupsTests.test_xor_four_children_counts xor_lookups.tests_llm.XorLookupsTests.test_xor_four_children_values_list xor_lookups.tests_llm.XorLookupsTests.test_xor_three_children_basic xor_lookups.tests_llm.XorLookupsTests.test_xor_three_children_complex_negation xor_lookups.tests_llm.XorLookupsTests.test_xor_three_children_empty_in_mix xor_lookups.tests_llm.XorLookupsTests.test_xor_three_children_exclude xor_lookups.tests_llm.XorLookupsTests.test_xor_three_children_negated_mix xor_lookups.tests_llm.XorLookupsTests.test_xor_three_children_overlap xor_lookups.tests_llm.XorLookupsTests.test_xor_three_children_pk_mix
coverage json -o coverage.json
: '>>>>> End Test Output'
