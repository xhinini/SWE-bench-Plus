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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.ManyToManyFormfieldForDBFieldRegressionTests.get_inner_widget admin_widgets.tests_llm.ManyToManyFormfieldForDBFieldRegressionTests.test_filter_horizontal_sets_filtered_widget admin_widgets.tests_llm.ManyToManyFormfieldForDBFieldRegressionTests.test_filter_vertical_sets_filtered_widget admin_widgets.tests_llm.ManyToManyFormfieldForDBFieldRegressionTests.test_formfield_overrides_widget_skips_get_autocomplete_fields admin_widgets.tests_llm.ManyToManyFormfieldForDBFieldRegressionTests.test_provided_widget_preserved_and_not_overwritten admin_widgets.tests_llm.ManyToManyFormfieldForDBFieldRegressionTests.test_widget_kwarg_skips_get_autocomplete_fields_request_none admin_widgets.tests_llm.ManyToManyFormfieldForDBFieldRegressionTests.test_widget_kwarg_skips_get_autocomplete_fields_request_object
coverage json -o coverage.json
: '>>>>> End Test Output'
