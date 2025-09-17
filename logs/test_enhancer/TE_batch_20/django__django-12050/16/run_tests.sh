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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueNested.test_deeply_nested_iterables_resolve_all_Fs queries.test_query_llm.TestResolveLookupValueNested.test_inner_non_expression_values_are_untouched queries.test_query_llm.TestResolveLookupValueNested.test_mixed_list_and_tuple_preserve_types_and_resolve queries.test_query_llm.TestResolveLookupValueNested.test_multiple_levels_mixed_types_resolve queries.test_query_llm.TestResolveLookupValueNested.test_nested_list_with_inner_list_and_Fs_resolves queries.test_query_llm.TestResolveLookupValueNested.test_nested_tuple_outer_preserved_and_inner_tuple_resolved queries.test_query_llm.TestResolveLookupValueNested.test_preserve_inner_list_when_outer_is_tuple queries.test_query_llm.TestResolveLookupValueNested.test_preserve_inner_tuple_when_outer_is_list queries.test_query_llm.TestResolveLookupValueNested.test_resolve_lookup_value_with_multiple_nested_levels_and_literals
coverage json -o coverage.json
: '>>>>> End Test Output'
