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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueNested.test_empty_inner_list_preserved queries.test_query_llm.TestResolveLookupValueNested.test_mixed_nested_values_resolve_and_preserve_values queries.test_query_llm.TestResolveLookupValueNested.test_mixed_tuple_list_tuple_deep_nested queries.test_query_llm.TestResolveLookupValueNested.test_multiple_Fs_in_inner_list_all_resolved queries.test_query_llm.TestResolveLookupValueNested.test_nested_list_resolves_F_to_simplecol queries.test_query_llm.TestResolveLookupValueNested.test_nested_tuple_list_preserves_types queries.test_query_llm.TestResolveLookupValueNested.test_nested_tuple_preserves_tuple_type_and_resolves queries.test_query_llm.TestResolveLookupValueNested.test_non_nested_iterable_behaviour_unchanged queries.test_query_llm.TestResolveLookupValueNested.test_simple_col_flag_false_resolves_to_Col queries.test_query_llm.TestResolveLookupValueNested.test_triple_nested_lists_resolve_deeply
coverage json -o coverage.json
: '>>>>> End Test Output'
