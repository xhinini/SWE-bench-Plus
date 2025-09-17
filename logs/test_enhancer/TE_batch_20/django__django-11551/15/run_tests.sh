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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.ListDisplayShadowingTests.setUp modeladmin.test_checks_llm.ListDisplayShadowingTests.tearDown modeladmin.test_checks_llm.ListDisplayShadowingTests.test_admin_method_overrides_model_field_and_is_valid modeladmin.test_checks_llm.ListDisplayShadowingTests.test_shadow_charfield_with_function_on_model_class_still_valid modeladmin.test_checks_llm.ListDisplayShadowingTests.test_shadow_m2m_in_second_position_reports_correct_label_and_e109 modeladmin.test_checks_llm.ListDisplayShadowingTests.test_shadow_m2m_with_callable_descriptor_on_model_class_raises_e109 modeladmin.test_checks_llm.ListDisplayShadowingTests.test_shadow_m2m_with_descriptor_raising_on_class_raises_e109 modeladmin.test_checks_llm.ListDisplayShadowingTests.test_shadow_m2m_with_function_on_model_class_raises_e109 modeladmin.test_checks_llm.ListDisplayShadowingTests.test_shadow_m2m_with_non_callable_on_model_class_raises_e109 modeladmin.test_checks_llm.ListDisplayShadowingTests.test_shadow_m2m_with_object_having_getattr_behavior_raises_e109 modeladmin.test_checks_llm.ListDisplayShadowingTests.test_shadow_m2m_with_property_on_model_class_raises_e109
coverage json -o coverage.json
: '>>>>> End Test Output'
