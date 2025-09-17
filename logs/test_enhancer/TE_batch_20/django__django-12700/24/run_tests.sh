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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.BadList.__new__ view_tests.tests.test_debug_llm.BadTuple.__new__ view_tests.tests.test_debug_llm.SafeExceptionReporterFilterListTupleSubclassTests.setUp view_tests.tests.test_debug_llm.SafeExceptionReporterFilterListTupleSubclassTests.test_badlist_empty_preserved view_tests.tests.test_debug_llm.SafeExceptionReporterFilterListTupleSubclassTests.test_badlist_mixed_types_preserved_and_cleansed view_tests.tests.test_debug_llm.SafeExceptionReporterFilterListTupleSubclassTests.test_badlist_nested_empty_structures_cleansed view_tests.tests.test_debug_llm.SafeExceptionReporterFilterListTupleSubclassTests.test_badlist_with_callable_element_wrapped view_tests.tests.test_debug_llm.SafeExceptionReporterFilterListTupleSubclassTests.test_list_subclass_in_dict_value_cleansed view_tests.tests.test_debug_llm.SafeExceptionReporterFilterListTupleSubclassTests.test_list_subclass_top_level_cleanses_inner_dict_password view_tests.tests.test_debug_llm.SafeExceptionReporterFilterListTupleSubclassTests.test_nested_list_subclass_with_tuple_inside_cleansed view_tests.tests.test_debug_llm.SafeExceptionReporterFilterListTupleSubclassTests.test_tuple_subclass_in_dict_value_cleansed view_tests.tests.test_debug_llm.SafeExceptionReporterFilterListTupleSubclassTests.test_tuple_subclass_top_level_cleanses_inner_dict
coverage json -o coverage.json
: '>>>>> End Test Output'
