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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.BaseGetInlinesRegressionTests.setUp generic_inline_admin.tests_llm.BaseGetInlinesRegressionTests.test_basemodeladmin_get_inlines_empty generic_inline_admin.tests_llm.BaseGetInlinesRegressionTests.test_basemodeladmin_get_inlines_returns_list generic_inline_admin.tests_llm.BaseGetInlinesRegressionTests.test_basemodeladmin_get_inlines_returns_tuple generic_inline_admin.tests_llm.BaseGetInlinesRegressionTests.test_basemodeladmin_get_inlines_with_None_value generic_inline_admin.tests_llm.InlineModelAdminGetInlinesRegressionTests.setUp generic_inline_admin.tests_llm.InlineModelAdminGetInlinesRegressionTests.test_basemodeladmin_and_inlinemodeladmin_independent_instances generic_inline_admin.tests_llm.InlineModelAdminGetInlinesRegressionTests.test_inlinemodeladmin_get_inlines_empty generic_inline_admin.tests_llm.InlineModelAdminGetInlinesRegressionTests.test_inlinemodeladmin_get_inlines_respects_attribute_set_late generic_inline_admin.tests_llm.InlineModelAdminGetInlinesRegressionTests.test_inlinemodeladmin_get_inlines_returns_list generic_inline_admin.tests_llm.InlineModelAdminGetInlinesRegressionTests.test_inlinemodeladmin_get_inlines_returns_tuple generic_inline_admin.tests_llm.InlineModelAdminGetInlinesRegressionTests.test_inlinemodeladmin_get_inlines_with_None_value
coverage json -o coverage.json
: '>>>>> End Test Output'
