#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.test_chained_filter_three_operands xor_lookups.tests_llm.test_empty_in_with_multiple_operands xor_lookups.tests_llm.test_exclude_three_operands xor_lookups.tests_llm.test_filter_four_operands xor_lookups.tests_llm.test_filter_three_operands xor_lookups.tests_llm.test_many_operands_compilation xor_lookups.tests_llm.test_negated_mixed_three xor_lookups.tests_llm.test_pk_q_multiple_operands xor_lookups.tests_llm.test_values_list_five_operands xor_lookups.tests_llm.test_where_as_sql_compiles_for_multiple_operands
coverage json -o coverage.json
: '>>>>> End Test Output'
