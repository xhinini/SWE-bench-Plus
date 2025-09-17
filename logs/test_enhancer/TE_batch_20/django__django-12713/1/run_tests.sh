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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.ManyToManyWidgetOverrideBugTests.test_explicit_widget_kwarg_and_autocomplete_declared admin_widgets.tests_llm.ManyToManyWidgetOverrideBugTests.test_explicit_widget_kwarg_instance admin_widgets.tests_llm.ManyToManyWidgetOverrideBugTests.test_formfield_overrides_widget_class admin_widgets.tests_llm.ManyToManyWidgetOverrideBugTests.test_formfield_overrides_widget_instance admin_widgets.tests_llm.ManyToManyWidgetOverrideBugTests.test_multiple_overrides_combination admin_widgets.tests_llm.ManyToManyWidgetOverrideBugTests.test_override_class_and_autocomplete_declared admin_widgets.tests_llm.ManyToManyWidgetOverrideBugTests.test_override_instance_and_autocomplete_declared admin_widgets.tests_llm.ManyToManyWidgetOverrideBugTests.test_override_with_filter_horizontal admin_widgets.tests_llm.ManyToManyWidgetOverrideBugTests.test_override_with_filter_vertical admin_widgets.tests_llm.ManyToManyWidgetOverrideBugTests.test_override_with_raw_id_fields admin_widgets.tests_llm._unwrap_widget
coverage json -o coverage.json
: '>>>>> End Test Output'
