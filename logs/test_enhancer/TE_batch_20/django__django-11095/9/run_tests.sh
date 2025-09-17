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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.GetInlinesRegressionTests.setUp generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_base_get_inlines_reflects_mutation generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_base_modeladmin_get_inlines_on_subclass_of_modeladmin generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_base_modeladmin_has_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inlines_is_bound_method generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inlines_not_shadowed_by_modeladmin_method generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_get_inlines_accepts_request_and_obj generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_get_inlines_with_fake_admin_site generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_instance_without_setting_inlines_attribute generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_modeladmin_has_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_multiple_instances_different_inlines
coverage json -o coverage.json
: '>>>>> End Test Output'
