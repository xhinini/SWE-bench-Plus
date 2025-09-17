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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_many_to_many_after_callable_reports_correct_index modeladmin.test_checks_llm.ListDisplayRegressionTests.test_many_to_many_field_index_0_reports_E109 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_many_to_many_field_index_1_reports_E109 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_many_to_many_field_index_2_reports_E109 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_missing_attribute_index_1_reports_E108 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_method_in_list_display_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_method_then_many_to_many_reports_E109_at_correct_index modeladmin.test_checks_llm.ListDisplayRegressionTests.test_multiple_many_to_many_fields_report_two_E109_errors modeladmin.test_checks_llm.ListDisplayRegressionTests.test_property_on_model_is_valid_in_list_display
coverage json -o coverage.json
: '>>>>> End Test Output'
