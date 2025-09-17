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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_autocomplete_field_with_formfield_override_preserve_widget admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_combined_widget_kwargs_and_overrides_preserve_widget admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_direct_call_preserve_widget_no_request admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_filter_horizontal_with_formfield_override_preserve_widget admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_filter_vertical_with_formfield_override_preserve_widget admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_formfield_overrides_preserve_widget_no_request admin_widgets.tests_llm.ManyToManyWidgetOverrideTests.test_raw_id_fields_with_formfield_override_preserve_widget admin_widgets.tests_llm._unwrap_widget
coverage json -o coverage.json
: '>>>>> End Test Output'
