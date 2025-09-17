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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.ListDisplayRegressionTests._check modeladmin.test_checks_llm.ListDisplayRegressionTests.test_admin_attribute_takes_precedence_over_model_many_to_many modeladmin.test_checks_llm.ListDisplayRegressionTests.test_admin_callable_function_in_list_display modeladmin.test_checks_llm.ListDisplayRegressionTests.test_descriptor_on_model_not_field_but_accessible_via_instance modeladmin.test_checks_llm.ListDisplayRegressionTests.test_many_to_many_still_flagged_even_if_descriptor_raises_on_class modeladmin.test_checks_llm.ListDisplayRegressionTests.test_mixed_items_reports_correct_labels_and_ids modeladmin.test_checks_llm.ListDisplayRegressionTests.test_model_method_callable_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_position_field_accessible_only_via_instance_is_valid modeladmin.test_checks_llm.ListDisplayRegressionTests.test_position_field_among_manytomany_and_nonexistent modeladmin.test_checks_llm.ListDisplayRegressionTests.test_property_on_model_class_valid
coverage json -o coverage.json
: '>>>>> End Test Output'
