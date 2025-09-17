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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.ManyToManyWidgetOverrideTests._unwrap_widget admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_selectmultiple_help_text_appended_when_selectmultiple_widget_provided admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_widget_in_formfield_overrides_overrides_autocomplete_setting admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_widget_in_formfield_overrides_prevents_get_autocomplete_call admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_widget_in_formfield_overrides_with_filter_horizontal_preserved admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_widget_in_formfield_overrides_with_raw_id_fields_preserved admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_widget_instance_preserved_when_passed_directly admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_widget_kwarg_overrides_autocomplete_setting admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_widget_kwarg_prevents_get_autocomplete_call admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_widget_kwarg_with_filter_vertical_preserved admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_widget_kwarg_with_raw_id_fields_preserved
coverage json -o coverage.json
: '>>>>> End Test Output'
