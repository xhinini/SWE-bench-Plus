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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueIterables.test_custom_list_subclass_preserves_type_and_resolves_nested queries.test_query_llm.TestResolveLookupValueIterables.test_deeply_nested_iterables_are_recursively_resolved queries.test_query_llm.TestResolveLookupValueIterables.test_mixed_list_and_tuple_nested_iterables queries.test_query_llm.TestResolveLookupValueIterables.test_nested_list_with_F_is_recursively_resolved queries.test_query_llm.TestResolveLookupValueIterables.test_nested_tuple_with_F_is_recursively_resolved_and_type_preserved queries.test_query_llm.TestResolveLookupValueIterables.test_non_F_expression_nested_in_iterable_is_resolved queries.test_query_llm.TestResolveLookupValueIterables.test_top_level_tuple_preserved_with_nested_list
coverage json -o coverage.json
: '>>>>> End Test Output'
