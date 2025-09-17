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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_basemodeladmin_subclass_has_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_generictabularinline_has_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inlines_accepts_obj_arg generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inlines_on_generic_inline_with_parent generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inlines_on_inline_respects_class_attr generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_modeladmin_get_inlines_direct_call generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_tabularinline_has_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_tabularinline_inlines_list_returned generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_tabularinline_inlines_tuple_returned
coverage json -o coverage.json
: '>>>>> End Test Output'
