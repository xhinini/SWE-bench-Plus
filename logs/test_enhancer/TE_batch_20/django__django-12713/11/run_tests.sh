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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.M2MWidgetKwargsTests._make_admin_that_errors_on_autocomplete admin_widgets.tests_llm.M2MWidgetKwargsTests._unwrap_widget admin_widgets.tests_llm.M2MWidgetKwargsTests.test_advisor_companies_widget_kwarg_no_request admin_widgets.tests_llm.M2MWidgetKwargsTests.test_advisor_companies_widget_kwarg_with_request admin_widgets.tests_llm.M2MWidgetKwargsTests.test_band_members_widget_kwarg_no_request admin_widgets.tests_llm.M2MWidgetKwargsTests.test_band_members_widget_kwarg_with_request admin_widgets.tests_llm.M2MWidgetKwargsTests.test_direct_formfield_for_manytomany_widget_kwarg_no_request admin_widgets.tests_llm.M2MWidgetKwargsTests.test_school_alumni_widget_kwarg_no_request admin_widgets.tests_llm.M2MWidgetKwargsTests.test_school_alumni_widget_kwarg_with_request admin_widgets.tests_llm.M2MWidgetKwargsTests.test_school_students_widget_kwarg_no_request admin_widgets.tests_llm.M2MWidgetKwargsTests.test_school_students_widget_kwarg_with_request
coverage json -o coverage.json
: '>>>>> End Test Output'
