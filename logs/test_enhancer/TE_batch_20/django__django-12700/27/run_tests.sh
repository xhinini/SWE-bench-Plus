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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.ListTupleSubclassTests.setUp view_tests.tests.test_debug_llm.ListTupleSubclassTests.test_list_subclass_empty view_tests.tests.test_debug_llm.ListTupleSubclassTests.test_list_subclass_nested_list_of_lists view_tests.tests.test_debug_llm.ListTupleSubclassTests.test_list_subclass_nested_sensitive_dict view_tests.tests.test_debug_llm.ListTupleSubclassTests.test_list_subclass_strings view_tests.tests.test_debug_llm.ListTupleSubclassTests.test_list_subclass_with_non_string_key_in_inner_dict view_tests.tests.test_debug_llm.ListTupleSubclassTests.test_namedtuple_mixed_nested_structures view_tests.tests.test_debug_llm.ListTupleSubclassTests.test_namedtuple_tuple_handling_sensitive_inner view_tests.tests.test_debug_llm.ListTupleSubclassTests.test_tuple_namedtuple_non_string_inner_key
coverage json -o coverage.json
: '>>>>> End Test Output'
