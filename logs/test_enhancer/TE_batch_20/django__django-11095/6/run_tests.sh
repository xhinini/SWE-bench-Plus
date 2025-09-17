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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.GetInlinesRegressionTests.setUp generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_base_model_admin_get_inlines_requires_obj_argument generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_base_model_admin_get_inlines_returns_inlines_attribute generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inline_instances_calls_get_inlines_with_passed_obj generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inlines_on_inline_instance_does_not_depend_on_modeladmin_only generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_model_admin_get_inlines_requires_obj_argument generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_model_admin_inherits_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_modeladmin_get_inlines_requires_obj_when_inherited_from_base generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_modeladmin_has_get_inlines_and_delegates_to_it_for_instances
coverage json -o coverage.json
: '>>>>> End Test Output'
