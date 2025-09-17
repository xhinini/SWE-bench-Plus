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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestQueryNestedResolve.test_deeply_nested_three_levels queries.test_query_llm.TestQueryNestedResolve.test_mixed_list_and_tuple_nested_resolves queries.test_query_llm.TestQueryNestedResolve.test_nested_list_of_f_resolves queries.test_query_llm.TestQueryNestedResolve.test_nested_mixed_values_and_f queries.test_query_llm.TestQueryNestedResolve.test_nested_tuple_of_f_resolves_and_preserves_type queries.test_query_llm.TestQueryNestedResolve.test_nested_tuple_of_lists_of_tuples
coverage json -o coverage.json
: '>>>>> End Test Output'
