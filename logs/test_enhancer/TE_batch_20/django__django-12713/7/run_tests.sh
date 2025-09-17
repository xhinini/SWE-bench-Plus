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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.ManyToManyWidgetProvidedTests._make_admin admin_widgets.tests_llm.ManyToManyWidgetProvidedTests.test_widget_instance_preserved_even_if_admin_has_autocomplete admin_widgets.tests_llm.ManyToManyWidgetProvidedTests.test_widget_provided_and_query_param_present admin_widgets.tests_llm.ManyToManyWidgetProvidedTests.test_widget_provided_basic_no_autocomplete_call admin_widgets.tests_llm.ManyToManyWidgetProvidedTests.test_widget_provided_with_callable_widget_instance admin_widgets.tests_llm.ManyToManyWidgetProvidedTests.test_widget_provided_with_empty_string_using admin_widgets.tests_llm.ManyToManyWidgetProvidedTests.test_widget_provided_with_filter_horizontal_not_overridden admin_widgets.tests_llm.ManyToManyWidgetProvidedTests.test_widget_provided_with_filter_vertical_not_overridden admin_widgets.tests_llm.ManyToManyWidgetProvidedTests.test_widget_provided_with_multiple_admin_flags admin_widgets.tests_llm.ManyToManyWidgetProvidedTests.test_widget_provided_with_raw_id_fields_not_overridden admin_widgets.tests_llm.ManyToManyWidgetProvidedTests.test_widget_provided_with_using_kwarg admin_widgets.tests_llm.RaisingAutocompleteAdmin.get_autocomplete_fields
coverage json -o coverage.json
: '>>>>> End Test Output'
