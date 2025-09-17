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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_lookup_value_deeply_nested_mixed_types queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_lookup_value_deeply_nested_three_levels queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_lookup_value_list_with_tuple_inner_preserves_inner_type queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_lookup_value_mixed_nested_iterables queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_lookup_value_multiple_levels_with_non_expressions queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_lookup_value_nested_list_resolves_inner_F queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_lookup_value_nested_tuple_resolves_inner_F queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_lookup_value_tuple_with_list_inner_preserves_inner_type
coverage json -o coverage.json
: '>>>>> End Test Output'
