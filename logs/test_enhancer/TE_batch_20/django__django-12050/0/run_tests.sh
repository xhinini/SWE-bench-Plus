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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValue.test_deeply_nested_list queries.test_query_llm.TestResolveLookupValue.test_mixed_nested_multiple queries.test_query_llm.TestResolveLookupValue.test_multiple_f_instances_nested queries.test_query_llm.TestResolveLookupValue.test_nested_list_in_tuple queries.test_query_llm.TestResolveLookupValue.test_nested_list_of_f queries.test_query_llm.TestResolveLookupValue.test_nested_mixed_tuple_list queries.test_query_llm.TestResolveLookupValue.test_nested_tuple_in_list queries.test_query_llm.TestResolveLookupValue.test_nested_tuple_of_f_preserves_outer_type queries.test_query_llm.TestResolveLookupValue.test_nested_value_and_f queries.test_query_llm.TestResolveLookupValue.test_nested_various_depths
coverage json -o coverage.json
: '>>>>> End Test Output'
