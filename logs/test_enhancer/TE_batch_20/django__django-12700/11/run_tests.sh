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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.RegressionSafeExceptionReporterFilterTests.setUp view_tests.tests.test_debug_llm.RegressionSafeExceptionReporterFilterTests.test_get_safe_settings_includes_cleansed_namedtuple view_tests.tests.test_debug_llm.RegressionSafeExceptionReporterFilterTests.test_list_of_namedtuples_cleansed view_tests.tests.test_debug_llm.RegressionSafeExceptionReporterFilterTests.test_mixed_namedtuple_and_plain_tuple_cleansed view_tests.tests.test_debug_llm.RegressionSafeExceptionReporterFilterTests.test_namedtuple_direct_cleansed view_tests.tests.test_debug_llm.RegressionSafeExceptionReporterFilterTests.test_namedtuple_inside_list_cleansed view_tests.tests.test_debug_llm.RegressionSafeExceptionReporterFilterTests.test_namedtuple_inside_tuple_cleansed view_tests.tests.test_debug_llm.RegressionSafeExceptionReporterFilterTests.test_namedtuple_nested_in_dict_value_cleansed view_tests.tests.test_debug_llm.RegressionSafeExceptionReporterFilterTests.test_nested_structures_with_namedtuple_cleansed view_tests.tests.test_debug_llm.RegressionSafeExceptionReporterFilterTests.test_tuple_of_namedtuples_cleansed view_tests.tests.test_debug_llm.RegressionSafeExceptionReporterFilterTests.test_tuple_subclass_with_strange_constructor_cleansed
coverage json -o coverage.json
: '>>>>> End Test Output'
