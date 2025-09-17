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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_descriptor_accessible_only_via_instance_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_missing_field_reports_admin_e108 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_attribute_named_like_field_but_not_field_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_callable_attribute_on_class_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_class_attribute_non_field_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_method_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_property_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_pk_in_list_display_is_valid
coverage json -o coverage.json
: '>>>>> End Test Output'
