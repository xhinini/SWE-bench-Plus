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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.AutocompleteFlaggingAdmin.get_autocomplete_fields admin_widgets.tests_llm.AutocompleteRaisingAdmin.get_autocomplete_fields admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_checkbox_widget_help_text_not_appended admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_get_autocomplete_not_called_when_widget_provided admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_preserve_custom_widget_when_autocomplete_field_list_nonempty admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_preserve_custom_widget_when_autocomplete_might_raise admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_preserve_custom_widget_with_filter_horizontal_configured admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_preserve_custom_widget_with_filter_vertical_configured admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_preserve_custom_widget_with_raw_id_field_configured admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_preserve_custom_widget_with_using_kwarg admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_selectmultiple_help_text_appended_only_when_no_custom_widget admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_widget_preserved_over_formfield_overrides
coverage json -o coverage.json
: '>>>>> End Test Output'
