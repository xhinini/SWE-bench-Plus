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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueNested.test_deeply_nested_resolves_F queries.test_query_llm.TestResolveLookupValueNested.test_empty_inner_sequence_preserved queries.test_query_llm.TestResolveLookupValueNested.test_mixed_list_tuple_preserves_types_and_resolves queries.test_query_llm.TestResolveLookupValueNested.test_nested_list_resolves_F_to_col queries.test_query_llm.TestResolveLookupValueNested.test_nested_multiple_Fs_resolved queries.test_query_llm.TestResolveLookupValueNested.test_nested_structures_with_multiple_levels_and_types queries.test_query_llm.TestResolveLookupValueNested.test_nested_tuple_resolves_F_to_col queries.test_query_llm.TestResolveLookupValueNested.test_non_expression_items_unchanged_inside_nested
coverage json -o coverage.json
: '>>>>> End Test Output'
