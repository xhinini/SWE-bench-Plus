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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestQueryResolveLookupValueNested.test_deep_mixed_nesting_resolves_all_expressions queries.test_query_llm.TestQueryResolveLookupValueNested.test_deep_uniform_list_nesting_resolves_all_levels queries.test_query_llm.TestQueryResolveLookupValueNested.test_mixed_values_and_expressions_in_nested_containers queries.test_query_llm.TestQueryResolveLookupValueNested.test_nested_list_inside_tuple_resolves_F queries.test_query_llm.TestQueryResolveLookupValueNested.test_nested_tuple_inside_list_resolves_F queries.test_query_llm.TestQueryResolveLookupValueNested.test_three_level_nesting_resolves_F_deeply queries.test_query_llm.TestQueryResolveLookupValueNested.test_tuple_of_lists_with_inner_Fs
coverage json -o coverage.json
: '>>>>> End Test Output'
