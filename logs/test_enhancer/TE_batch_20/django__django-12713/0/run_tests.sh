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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_formfield_for_manytomany_direct_call_with_widget_kwarg admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_instance_preserved_no_help_text_appended admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_kwarg_preserved_basic admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_kwarg_preserved_even_if_autocomplete_would_match admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_kwarg_preserved_with_both_filters admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_kwarg_preserved_with_filter_horizontal admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_kwarg_preserved_with_filter_vertical admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_kwarg_preserved_with_raw_id_field_setting admin_widgets.tests_llm.ManyToManyWidgetKwargTests.test_widget_kwarg_preserved_with_unrelated_admin_settings admin_widgets.tests_llm._unwrap_widget
coverage json -o coverage.json
: '>>>>> End Test Output'
