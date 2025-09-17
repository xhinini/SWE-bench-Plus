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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.TestGetInlinesRegression.setUp generic_inline_admin.tests_llm.TestGetInlinesRegression.test_basemodeladmin_default_get_inlines_returns_attribute generic_inline_admin.tests_llm.TestGetInlinesRegression.test_basemodeladmin_get_inlines_without_obj_argument generic_inline_admin.tests_llm.TestGetInlinesRegression.test_basemodeladmin_super_call_in_subclass generic_inline_admin.tests_llm.TestGetInlinesRegression.test_deep_inheritance_super_chain_calls_base generic_inline_admin.tests_llm.TestGetInlinesRegression.test_inlinemodeladmin_default_get_inlines_returns_attribute generic_inline_admin.tests_llm.TestGetInlinesRegression.test_inlinemodeladmin_get_inlines_bound_as_method generic_inline_admin.tests_llm.TestGetInlinesRegression.test_inlinemodeladmin_super_call_in_subclass generic_inline_admin.tests_llm.TestGetInlinesRegression.test_modeladmin_get_inline_instances_no_inlines_for_obj generic_inline_admin.tests_llm.TestGetInlinesRegression.test_modeladmin_get_inline_instances_returns_instances_when_get_inlines_nonempty
coverage json -o coverage.json
: '>>>>> End Test Output'
