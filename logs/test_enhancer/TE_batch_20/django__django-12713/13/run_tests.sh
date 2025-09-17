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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_direct_widget_kwarg_honored_basic admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_direct_widget_kwarg_honored_with_autocomplete_fields admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_direct_widget_kwarg_honored_with_filter_horizontal admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_direct_widget_kwarg_honored_with_filter_vertical admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_direct_widget_kwarg_honored_with_raw_id_setting admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_formfield_overrides_widget_honored_basic admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_formfield_overrides_widget_honored_with_autocomplete_fields admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_formfield_overrides_widget_honored_with_filter_horizontal admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_formfield_overrides_widget_honored_with_filter_vertical admin_widgets.tests_llm.FormfieldForManyToManyWidgetOverrideTests.test_formfield_overrides_widget_honored_with_raw_id_setting admin_widgets.tests_llm.GetAutocompleteRaisesIfRequestNoneAdmin.get_autocomplete_fields admin_widgets.tests_llm._inner_widget
coverage json -o coverage.json
: '>>>>> End Test Output'
