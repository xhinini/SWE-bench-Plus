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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestQueryResolveLookupValueNested.test_deeply_nested_three_levels queries.test_query_llm.TestQueryResolveLookupValueNested.test_mixed_nested_iterables_resolve_all_f_instances queries.test_query_llm.TestQueryResolveLookupValueNested.test_mixed_none_and_f_in_nested_iterables queries.test_query_llm.TestQueryResolveLookupValueNested.test_nested_iterables_with_multiple_f_instances_all_resolved queries.test_query_llm.TestQueryResolveLookupValueNested.test_nested_list_of_f_resolves_inner_to_col queries.test_query_llm.TestQueryResolveLookupValueNested.test_nested_tuple_and_list_combination_preserves_types_and_resolves queries.test_query_llm.TestQueryResolveLookupValueNested.test_nested_tuple_of_f_resolves_inner_to_col_and_preserves_tuple_types
coverage json -o coverage.json
: '>>>>> End Test Output'
