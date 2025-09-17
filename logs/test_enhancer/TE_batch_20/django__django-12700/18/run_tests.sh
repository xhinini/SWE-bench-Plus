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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests._make_bad_tuple_class view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_badtuple_empty_sequence view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_badtuple_in_list_cleansed view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_badtuple_multiple_elements_cleansed view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_badtuple_nested_in_dict_cleansed view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_badtuple_setting_inner_sensitive_cleansed view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_badtuple_with_non_str_key_inside_dict_does_not_raise view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_callable_inside_tuple_subclass_wrapped view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_deeply_nested_badtuple_handles_gracefully view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_namedtuple_in_setting_cleansed view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_tuple_subclass_parent_key_token_matches
coverage json -o coverage.json
: '>>>>> End Test Output'
