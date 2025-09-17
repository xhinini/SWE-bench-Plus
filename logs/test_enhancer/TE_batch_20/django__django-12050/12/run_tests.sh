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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueNested.test_deep_three_level_tuple_list_tuple queries.test_query_llm.TestResolveLookupValueNested.test_deeply_nested_mixed_containers queries.test_query_llm.TestResolveLookupValueNested.test_list_inside_tuple_with_F queries.test_query_llm.TestResolveLookupValueNested.test_mixed_nested_empty_and_expressions queries.test_query_llm.TestResolveLookupValueNested.test_multiple_nested_elements_mixed queries.test_query_llm.TestResolveLookupValueNested.test_nested_list_with_F queries.test_query_llm.TestResolveLookupValueNested.test_nested_tuple_inside_list_with_F queries.test_query_llm.TestResolveLookupValueNested.test_preserve_outer_type_list_of_tuple queries.test_query_llm.TestResolveLookupValueNested.test_preserve_outer_type_tuple_of_list queries.test_query_llm.TestResolveLookupValueNested.test_tuple_of_tuple_with_F
coverage json -o coverage.json
: '>>>>> End Test Output'
