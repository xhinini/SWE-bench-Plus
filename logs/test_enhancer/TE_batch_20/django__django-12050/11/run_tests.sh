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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueNested.test_resolve_lookup_value_deep_nesting queries.test_query_llm.TestResolveLookupValueNested.test_resolve_lookup_value_mixed_nested_structures queries.test_query_llm.TestResolveLookupValueNested.test_resolve_lookup_value_multiple_inner_items queries.test_query_llm.TestResolveLookupValueNested.test_resolve_lookup_value_nested_iterables_in_build_filter queries.test_query_llm.TestResolveLookupValueNested.test_resolve_lookup_value_nested_list_resolves_F queries.test_query_llm.TestResolveLookupValueNested.test_resolve_lookup_value_nested_tuple_in_list queries.test_query_llm.TestResolveLookupValueNested.test_resolve_lookup_value_nested_tuple_resolves_F queries.test_query_llm.TestResolveLookupValueNested.test_resolve_lookup_value_preserves_list_type_with_nested queries.test_query_llm.TestResolveLookupValueNested.test_resolve_lookup_value_preserves_tuple_type_with_nested
coverage json -o coverage.json
: '>>>>> End Test Output'
