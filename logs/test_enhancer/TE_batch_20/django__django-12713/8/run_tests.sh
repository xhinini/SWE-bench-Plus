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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.AdminThatErrorsOnNone.get_autocomplete_fields admin_widgets.tests_llm.FormfieldForManyToManyWidgetKwargTests._inner_widget admin_widgets.tests_llm.FormfieldForManyToManyWidgetKwargTests.test_advisor_companies_with_explicit_widget admin_widgets.tests_llm.FormfieldForManyToManyWidgetKwargTests.test_band_members_with_explicit_widget admin_widgets.tests_llm.FormfieldForManyToManyWidgetKwargTests.test_event_supporting_bands_with_explicit_widget admin_widgets.tests_llm.FormfieldForManyToManyWidgetKwargTests.test_school_alumni_with_select_multiple_widget admin_widgets.tests_llm.FormfieldForManyToManyWidgetKwargTests.test_school_students_with_filtered_widget_instance admin_widgets.tests_llm.FormfieldForManyToManyWidgetKwargTests.test_widget_kwarg_multiple_models_various_widgets admin_widgets.tests_llm.FormfieldForManyToManyWidgetKwargTests.test_widget_kwarg_when_filter_vertical_contains_field admin_widgets.tests_llm.FormfieldForManyToManyWidgetKwargTests.test_widget_kwarg_when_raw_id_fields_attribute_set admin_widgets.tests_llm.FormfieldForManyToManyWidgetKwargTests.test_widget_kwarg_with_queryset_parameter admin_widgets.tests_llm.FormfieldForManyToManyWidgetKwargTests.test_widget_kwarg_with_using_parameter
coverage json -o coverage.json
: '>>>>> End Test Output'
