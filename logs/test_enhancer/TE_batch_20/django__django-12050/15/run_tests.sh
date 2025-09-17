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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.ResolveLookupValueTests.test_deeply_nested_mixed_structures_resolve_all_Fs queries.test_query_llm.ResolveLookupValueTests.test_list_with_inner_tuple_resolves_inner_tuple_F queries.test_query_llm.ResolveLookupValueTests.test_mixed_expressions_and_literals_in_list queries.test_query_llm.ResolveLookupValueTests.test_nested_list_resolves_inner_list_F queries.test_query_llm.ResolveLookupValueTests.test_various_nested_combinations_resolve_all_Fs
coverage json -o coverage.json
: '>>>>> End Test Output'
