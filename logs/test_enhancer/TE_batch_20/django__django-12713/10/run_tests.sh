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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_autocomplete_used_when_no_widget_and_get_autocomplete_called admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_autocomplete_with_using_when_no_widget admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_direct_widget_prevents_get_autocomplete_call admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_direct_widget_with_using_prevents_get_autocomplete_call admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_filter_vertical_ignored_when_widget_supplied_directly admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_formfield_overrides_widget_class_prevents_get_autocomplete_call admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_formfield_overrides_widget_instance_prevents_get_autocomplete_call admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_raw_id_fields_ignored_when_widget_supplied_directly admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_widget_in_kwargs_with_filter_vertical_and_using
coverage json -o coverage.json
: '>>>>> End Test Output'
