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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.CleanseListTupleEmptyKeyTests.test_list_of_callables_with_empty_key_gets_masked view_tests.tests.test_debug_llm.CleanseListTupleEmptyKeyTests.test_list_recursion_uses_empty_key view_tests.tests.test_debug_llm.CleanseListTupleEmptyKeyTests.test_nested_list_recursion_uses_empty_key view_tests.tests.test_debug_llm.CleanseListTupleEmptyKeyTests.test_tuple_of_callables_with_empty_key_gets_masked view_tests.tests.test_debug_llm.CleanseListTupleEmptyKeyTests.test_tuple_recursion_uses_empty_key
coverage json -o coverage.json
: '>>>>> End Test Output'
