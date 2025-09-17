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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueNested.test_deeply_nested_lists queries.test_query_llm.TestResolveLookupValueNested.test_mixed_inner_types queries.test_query_llm.TestResolveLookupValueNested.test_multiple_exprs_in_nested_structure queries.test_query_llm.TestResolveLookupValueNested.test_nested_list_of_f queries.test_query_llm.TestResolveLookupValueNested.test_nested_mixed_depth_and_types queries.test_query_llm.TestResolveLookupValueNested.test_nested_tuple_of_f queries.test_query_llm.TestResolveLookupValueNested.test_nested_with_nonexprs_preserved queries.test_query_llm.TestResolveLookupValueNested.test_preserve_inner_tuple_type
coverage json -o coverage.json
: '>>>>> End Test Output'
