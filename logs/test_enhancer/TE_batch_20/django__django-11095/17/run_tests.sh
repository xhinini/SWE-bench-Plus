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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.DummyRequest.__init__ generic_inline_admin.tests_llm.DummyUser.has_perm generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_basemodeladmin_default_get_inlines_returns_inlines_attr generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_basemodeladmin_has_get_inlines_method generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inline_instances_filters_based_on_permissions generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inline_instances_sets_max_num_zero_when_no_add_permission generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inlines_accepts_tuple_return_types generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inlines_default_from_basemodeladmin_used_when_not_overridden generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inlinemodeladmin_inherits_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_modeladmin_get_inline_instances_uses_get_inlines_override
coverage json -o coverage.json
: '>>>>> End Test Output'
