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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_admin_non_callable_attribute_masks_many_to_many_and_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_field_descriptor_on_model_class_but_not_a_model_field_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_list_display_multiple_items_mixed_fields_and_methods modeladmin.test_checks_llm.ListDisplayRegressionTests.test_many_to_many_field_in_list_display_errors_E109 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_missing_field_reports_admin_E108 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_class_callable_returned_by_getattr_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_method_in_list_display_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_property_in_list_display_is_valid
coverage json -o coverage.json
: '>>>>> End Test Output'
