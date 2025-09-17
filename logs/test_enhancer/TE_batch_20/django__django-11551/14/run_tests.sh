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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.AdditionalListDisplayEdgeCases.test_attribute_of_model_class_that_is_not_callable_nor_field_errors modeladmin.test_checks_llm.AdditionalListDisplayEdgeCases.test_callable_attribute_on_model_class_is_valid modeladmin.test_checks_llm.AdditionalListDisplayEdgeCases.test_descriptor_raising_on_class_but_field_in_meta_is_handled modeladmin.test_checks_llm.AdditionalListDisplayEdgeCases.test_m2m_field_masked_by_class_attribute_still_detected modeladmin.test_checks_llm.AdditionalListDisplayEdgeCases.test_many_to_many_field_detected_even_if_getattr_returns_descriptor modeladmin.test_checks_llm.AdditionalListDisplayEdgeCases.test_method_on_model_is_valid_list_display modeladmin.test_checks_llm.AdditionalListDisplayEdgeCases.test_missing_nonexistent_attribute_reports_admin_e108 modeladmin.test_checks_llm.AdditionalListDisplayEdgeCases.test_property_on_model_is_valid_list_display
coverage json -o coverage.json
: '>>>>> End Test Output'
