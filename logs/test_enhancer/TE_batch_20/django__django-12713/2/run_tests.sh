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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.ManyToManyWidgetPreservationTests._unwrap_widget admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_explicit_widget_kwarg_preserved_with_filter_horizontal admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_explicit_widget_kwarg_preserved_with_filter_vertical admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_explicit_widget_kwarg_preserved_with_raw_id_fields admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_explicit_widget_kwarg_preserved_without_any_admin_flags admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_overrides_preserved_with_filter_horizontal admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_overrides_preserved_with_filter_horizontal_and_explicit_kwarg admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_overrides_preserved_with_filter_vertical admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_overrides_preserved_with_raw_id_fields admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_overrides_with_widget_class_preserved_filter_vertical admin_widgets.tests_llm.ManyToManyWidgetPreservationTests.test_overrides_with_widget_class_preserved_raw_id
coverage json -o coverage.json
: '>>>>> End Test Output'
