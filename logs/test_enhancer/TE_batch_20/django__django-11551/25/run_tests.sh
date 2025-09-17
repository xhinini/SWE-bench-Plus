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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_callable_object_and_many_to_many_and_missing modeladmin.test_checks_llm.ListDisplayRegressionTests.test_class_attribute_is_valid_in_list_display modeladmin.test_checks_llm.ListDisplayRegressionTests.test_descriptor_accessible_only_via_instance_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_many_to_many_error_obj_is_admin_class_and_message_and_id modeladmin.test_checks_llm.ListDisplayRegressionTests.test_many_to_many_field_reports_admin_E109 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_many_to_many_then_missing_produces_E109_then_E108 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_missing_field_reports_proper_model_app_label_and_object_name modeladmin.test_checks_llm.ListDisplayRegressionTests.test_missing_then_many_to_many_produces_E108_then_E109 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_method_name_as_string_is_valid modeladmin.test_checks_llm.PositionField.__get__ modeladmin.test_checks_llm.PositionField.contribute_to_class modeladmin.test_checks_llm.PositionField.db_type modeladmin.test_checks_llm.PositionField.deconstruct
coverage json -o coverage.json
: '>>>>> End Test Output'
