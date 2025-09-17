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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.GetInlinesRegressionTests.setUp generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inlines_is_callable_on_inline_class_instances_created_with_adminsite generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_get_inlines_accepts_obj_parameter generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_get_inlines_respects_instance_inlines_attribute generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_instance_get_inlines_and_modeladmin_get_inlines_are_independent generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_stackedinline_has_get_inlines_method generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_tabularinline_has_get_inlines_method
coverage json -o coverage.json
: '>>>>> End Test Output'
