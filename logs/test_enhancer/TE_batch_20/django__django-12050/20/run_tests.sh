#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueRecursive.test_deeply_nested_three_levels queries.test_query_llm.TestResolveLookupValueRecursive.test_empty_and_nonempty_nested_lists queries.test_query_llm.TestResolveLookupValueRecursive.test_list_of_tuple_with_f_inside_tuple queries.test_query_llm.TestResolveLookupValueRecursive.test_mixed_nested_structures queries.test_query_llm.TestResolveLookupValueRecursive.test_nested_list_of_list_with_f queries.test_query_llm.TestResolveLookupValueRecursive.test_nested_tuple_of_tuple_with_f queries.test_query_llm.TestResolveLookupValueRecursive.test_nested_tuples_with_mixed_types queries.test_query_llm.TestResolveLookupValueRecursive.test_non_expression_elements_preserved queries.test_query_llm.TestResolveLookupValueRecursive.test_simple_col_flag_false_resolves_to_col queries.test_query_llm.TestResolveLookupValueRecursive.test_tuple_of_list_with_f_inside_list
coverage json -o coverage.json
: '>>>>> End Test Output'
