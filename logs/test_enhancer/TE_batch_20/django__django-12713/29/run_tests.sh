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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.WidgetKwArgPreserveTests._inner_widget admin_widgets.tests_llm.WidgetKwArgPreserveTests.test_widget_kw_preserved_default_request_dummy admin_widgets.tests_llm.WidgetKwArgPreserveTests.test_widget_kw_preserved_default_request_none admin_widgets.tests_llm.WidgetKwArgPreserveTests.test_widget_kw_preserved_different_model_request_dummy admin_widgets.tests_llm.WidgetKwArgPreserveTests.test_widget_kw_preserved_different_model_request_none admin_widgets.tests_llm.WidgetKwArgPreserveTests.test_widget_kw_preserved_with_filter_horizontal_request_dummy admin_widgets.tests_llm.WidgetKwArgPreserveTests.test_widget_kw_preserved_with_filter_horizontal_request_none admin_widgets.tests_llm.WidgetKwArgPreserveTests.test_widget_kw_preserved_with_filter_vertical_request_dummy admin_widgets.tests_llm.WidgetKwArgPreserveTests.test_widget_kw_preserved_with_filter_vertical_request_none admin_widgets.tests_llm.WidgetKwArgPreserveTests.test_widget_kw_preserved_with_raw_id_request_dummy admin_widgets.tests_llm.WidgetKwArgPreserveTests.test_widget_kw_preserved_with_raw_id_request_none
coverage json -o coverage.json
: '>>>>> End Test Output'
