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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_admin_attribute_recognized_as_valid_list_display_entry modeladmin.test_checks_llm.ListDisplayRegressionTests.test_admin_method_name_in_list_display_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_callable_in_list_display_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_descriptor_accessible_only_via_instance_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_descriptor_not_registered_in_meta_raises_e108 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_detect_many_to_many_field_in_list_display modeladmin.test_checks_llm.ListDisplayRegressionTests.test_many_to_many_attached_as_class_attribute_not_in_meta_triggers_e109 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_missing_nonexistent_field_reports_e108 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_property_in_list_display_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_property_on_model_and_admin_mixed_entries
coverage json -o coverage.json
: '>>>>> End Test Output'
