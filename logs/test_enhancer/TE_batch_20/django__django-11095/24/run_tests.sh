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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.GetInlinesAPITest.test_base_modeladmin_has_get_inlines generic_inline_admin.tests_llm.GetInlinesAPITest.test_custom_tabular_inline_subclass_has_get_inlines generic_inline_admin.tests_llm.GetInlinesAPITest.test_generic_tabular_inline_has_get_inlines generic_inline_admin.tests_llm.GetInlinesAPITest.test_get_inlines_is_callable_on_inline_and_modeladmin_instances generic_inline_admin.tests_llm.GetInlinesAPITest.test_inlinemodeladmin_has_get_inlines generic_inline_admin.tests_llm.GetInlinesAPITest.test_mediainline_instance_has_get_inlines generic_inline_admin.tests_llm.GetInlinesAPITest.test_mediapermanentinline_instance_has_get_inlines generic_inline_admin.tests_llm.GetInlinesAPITest.test_modeladmin_get_inlines_returns_inlines_attribute generic_inline_admin.tests_llm.GetInlinesAPITest.test_modeladmin_has_get_inlines generic_inline_admin.tests_llm.GetInlinesAPITest.test_tabular_and_stacked_inlines_have_get_inlines
coverage json -o coverage.json
: '>>>>> End Test Output'
