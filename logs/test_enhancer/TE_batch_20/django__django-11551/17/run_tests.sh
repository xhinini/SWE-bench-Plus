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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.AdditionalListDisplayChecks._errors_for modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_admin_function_object_in_list_display_is_valid modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_class_attribute_on_model_allowed_in_list_display modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_descriptor_accessible_only_via_instance_but_registered_as_field modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_descriptor_on_class_which_is_not_a_field_raises_admin_e108 modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_many_to_many_in_list_display_returns_admin_e109 modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_missing_field_in_list_display_returns_admin_e108 modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_model_method_in_list_display_is_valid modeladmin.test_checks_llm.AdditionalListDisplayChecks.test_model_property_in_list_display_is_valid
coverage json -o coverage.json
: '>>>>> End Test Output'
