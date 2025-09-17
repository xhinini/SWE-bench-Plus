#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.AdditionalXorTests._disable_xor_feature xor_lookups.tests_llm.AdditionalXorTests._restore_xor_feature xor_lookups.tests_llm.AdditionalXorTests.setUpTestData xor_lookups.tests_llm.AdditionalXorTests.test_empty_in_multiple xor_lookups.tests_llm.AdditionalXorTests.test_exclude_multiple xor_lookups.tests_llm.AdditionalXorTests.test_five_xor_qs xor_lookups.tests_llm.AdditionalXorTests.test_negated_whole_multiple xor_lookups.tests_llm.AdditionalXorTests.test_pk_q_three xor_lookups.tests_llm.AdditionalXorTests.test_stages_multiple xor_lookups.tests_llm.AdditionalXorTests.test_three_xor_qs xor_lookups.tests_llm.AdditionalXorTests.test_three_xor_with_negation xor_lookups.tests_llm.AdditionalXorTests.test_values_list_multiple
coverage json -o coverage.json
: '>>>>> End Test Output'
