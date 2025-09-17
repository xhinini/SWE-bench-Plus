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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.ListDisplayRegressionTests.test_class_level_attribute_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_descriptor_only_on_instance_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_manager_attribute_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_many_to_many_error_single modeladmin.test_checks_llm.ListDisplayRegressionTests.test_mixed_admin_and_model_attributes modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_method_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_multiple_list_display_errors modeladmin.test_checks_llm.ListDisplayRegressionTests.test_nonexistent_item_error modeladmin.test_checks_llm.ListDisplayRegressionTests.test_property_attribute_is_valid
coverage json -o coverage.json
: '>>>>> End Test Output'
