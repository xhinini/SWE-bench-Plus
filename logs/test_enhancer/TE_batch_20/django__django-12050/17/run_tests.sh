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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestQueryNestedResolveLookupValue.test_deep_tuple_and_list_mixture_resolves queries.test_query_llm.TestQueryNestedResolveLookupValue.test_empty_inner_iterable_preserved queries.test_query_llm.TestQueryNestedResolveLookupValue.test_list_with_inner_tuple_preserves_inner_type queries.test_query_llm.TestQueryNestedResolveLookupValue.test_mixed_literals_and_expressions_in_inner_iterable queries.test_query_llm.TestQueryNestedResolveLookupValue.test_mixed_nested_iterables_resolve_all_expressions queries.test_query_llm.TestQueryNestedResolveLookupValue.test_nested_depth3_resolves_deep_expression queries.test_query_llm.TestQueryNestedResolveLookupValue.test_nested_list_depth2_resolves_F queries.test_query_llm.TestQueryNestedResolveLookupValue.test_nested_tuple_depth2_resolves_F queries.test_query_llm.TestQueryNestedResolveLookupValue.test_tuple_with_inner_list_preserves_inner_type
coverage json -o coverage.json
: '>>>>> End Test Output'
