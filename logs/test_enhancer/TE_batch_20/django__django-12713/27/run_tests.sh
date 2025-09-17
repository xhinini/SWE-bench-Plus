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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.ManyToManyWidgetOverrideGuardTests._guard_admin_class admin_widgets.tests_llm.ManyToManyWidgetOverrideGuardTests._unwrap_widget admin_widgets.tests_llm.ManyToManyWidgetOverrideGuardTests.test_combined_formfield_overrides_and_raw_id_does_not_call_autocomplete admin_widgets.tests_llm.ManyToManyWidgetOverrideGuardTests.test_direct_manytomany_widget_kwarg_instance admin_widgets.tests_llm.ManyToManyWidgetOverrideGuardTests.test_direct_manytomany_widget_kwarg_instance_multiple_calls admin_widgets.tests_llm.ManyToManyWidgetOverrideGuardTests.test_formfield_overrides_widget_class_and_kwarg_priority admin_widgets.tests_llm.ManyToManyWidgetOverrideGuardTests.test_formfield_overrides_widget_class_in_admin admin_widgets.tests_llm.ManyToManyWidgetOverrideGuardTests.test_formfield_overrides_widget_instance_in_admin admin_widgets.tests_llm.ManyToManyWidgetOverrideGuardTests.test_manytomany_widget_kwarg_via_formfield_for_dbfield admin_widgets.tests_llm.ManyToManyWidgetOverrideGuardTests.test_widget_kwarg_with_filter_horizontal_present admin_widgets.tests_llm.ManyToManyWidgetOverrideGuardTests.test_widget_kwarg_with_filter_vertical_present admin_widgets.tests_llm.ManyToManyWidgetOverrideGuardTests.test_widget_kwarg_with_raw_id_fields_present
coverage json -o coverage.json
: '>>>>> End Test Output'
