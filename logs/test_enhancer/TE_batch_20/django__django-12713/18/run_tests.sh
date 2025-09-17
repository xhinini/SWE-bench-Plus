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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.ManyToManyWidgetKwargTests._make_admin admin_widgets.tests_llm.ManyToManyWidgetKwargTests.setUp admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_kwarg_prevents_autocomplete_being_called admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_kwarg_with_autocomplete_as_method_raising admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_kwarg_with_autocomplete_tuple_and_instance_widget admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_kwarg_with_filter_vertical_does_not_invoke_autocomplete admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_kwarg_with_raw_id_fields_does_not_invoke_autocomplete admin_widgets.tests_llm.ManyToManyWidgetPreservationSimpleTests.setUp admin_widgets.tests_llm.ManyToManyWidgetPreservationSimpleTests.test_autocomplete_widget_selected_when_no_widget_kwarg admin_widgets.tests_llm.ManyToManyWidgetPreservationSimpleTests.test_formfield_overrides_widget_wins_over_filter_vertical admin_widgets.tests_llm.ManyToManyWidgetPreservationSimpleTests.test_selectmultiple_help_text_appended_when_user_widget_is_selectmultiple admin_widgets.tests_llm.ManyToManyWidgetPreservationSimpleTests.test_widget_kwarg_with_query_set_preserved
coverage json -o coverage.json
: '>>>>> End Test Output'
