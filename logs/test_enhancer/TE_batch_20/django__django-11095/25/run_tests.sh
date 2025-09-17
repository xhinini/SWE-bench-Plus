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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.GetInlinesRegressionTests.setUp generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_01_base_model_admin_has_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_02_inline_model_admin_inherits_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_04_get_inline_instances_respects_override_returning_list generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_05_get_inline_instances_respects_override_returning_tuple generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_06_get_inlines_can_return_generator generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_07_get_inlines_receives_obj_parameter generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_10_baseclass_method_is_callable_on_instances
coverage json -o coverage.json
: '>>>>> End Test Output'
