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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.AdditionalListDisplayChecks.assert_check_result modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_admin_and_model_name_collision_prefers_admin_attr modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_admin_class_method_is_valid_in_list_display modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_descriptor_only_accessible_via_instance_is_valid modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_descriptor_raising_attribute_error_but_field_of_same_name_invalid modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_many_to_many_field_detected_as_invalid_for_list_display modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_missing_attribute_raises_E108_when_not_a_field_or_admin_attr modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_model_attribute_that_is_a_function_is_valid modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_model_class_callable_attribute_is_valid modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_property_on_model_class_is_valid_list_display_entry
coverage json -o coverage.json
: '>>>>> End Test Output'
