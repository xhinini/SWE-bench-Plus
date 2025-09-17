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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.GetInlinesRegressionTests.setUp generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_base_get_inlines_callable_from_instances_of_subclasses generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_base_model_admin_get_inlines_returns_tuple generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_base_model_admin_has_get_inlines_and_returns_list generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_modeladmin_get_inline_instances_honours_empty_list_from_base_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_modeladmin_get_inline_instances_passes_obj_to_base_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_modeladmin_get_inline_instances_passes_request_to_base_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_modeladmin_get_inline_instances_uses_base_get_inlines_monkeypatched_returning_list generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_modeladmin_get_inline_instances_uses_base_get_inlines_monkeypatched_returning_tuple generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_monkeypatched_base_get_inlines_can_return_different_inlines_per_call
coverage json -o coverage.json
: '>>>>> End Test Output'
