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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.AdditionalListDisplayTests.test_admin_method_name_in_list_display_is_valid modeladmin.test_checks_llm.AdditionalListDisplayTests.test_callable_in_list_display_is_valid modeladmin.test_checks_llm.AdditionalListDisplayTests.test_custom_field_descriptor_raises_on_class_access_is_valid modeladmin.test_checks_llm.AdditionalListDisplayTests.test_descriptor_raising_attributeerror_on_class_access_is_reported_missing modeladmin.test_checks_llm.AdditionalListDisplayTests.test_descriptor_returning_value_on_class_access_is_valid modeladmin.test_checks_llm.AdditionalListDisplayTests.test_many_to_many_field_detected_as_invalid modeladmin.test_checks_llm.AdditionalListDisplayTests.test_model_method_counts_as_attribute_valid modeladmin.test_checks_llm.AdditionalListDisplayTests.test_model_property_counts_as_attribute_valid modeladmin.test_checks_llm.AdditionalListDisplayTests.test_nonfield_class_attribute_valid
coverage json -o coverage.json
: '>>>>> End Test Output'
