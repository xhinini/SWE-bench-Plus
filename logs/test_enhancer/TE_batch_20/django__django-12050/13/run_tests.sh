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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueNested._assert_no_unresolved_F_and_has_simplecol queries.test_query_llm.TestResolveLookupValueNested._find_in_nested queries.test_query_llm.TestResolveLookupValueNested.test_deeply_nested_f queries.test_query_llm.TestResolveLookupValueNested.test_list_of_tuples_resolves_F queries.test_query_llm.TestResolveLookupValueNested.test_mixed_list_tuple_nested queries.test_query_llm.TestResolveLookupValueNested.test_nested_empty_and_f_resolves_F queries.test_query_llm.TestResolveLookupValueNested.test_nested_list_with_F queries.test_query_llm.TestResolveLookupValueNested.test_nested_multiple_Fs queries.test_query_llm.TestResolveLookupValueNested.test_nested_tuple_inside_list_resolves_F queries.test_query_llm.TestResolveLookupValueNested.test_nested_tuple_with_F queries.test_query_llm.TestResolveLookupValueNested.test_tuple_of_lists_resolves_F queries.test_query_llm.TestResolveLookupValueNested.test_various_depths_resolves_F
coverage json -o coverage.json
: '>>>>> End Test Output'
