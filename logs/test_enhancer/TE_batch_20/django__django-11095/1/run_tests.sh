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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.GetInlinesHookTests.setUp generic_inline_admin.tests_llm.GetInlinesHookTests.test_base_model_admin_has_get_inlines_and_returns_inlines generic_inline_admin.tests_llm.GetInlinesHookTests.test_generic_tabular_inline_has_get_inlines_and_returns_inlines generic_inline_admin.tests_llm.GetInlinesHookTests.test_get_inline_instances_receives_obj_passed_to_get_inlines generic_inline_admin.tests_llm.GetInlinesHookTests.test_get_inline_instances_uses_get_inlines generic_inline_admin.tests_llm.GetInlinesHookTests.test_get_inlines_accepts_obj_argument_on_base generic_inline_admin.tests_llm.GetInlinesHookTests.test_get_inlines_accepts_obj_argument_on_inline generic_inline_admin.tests_llm.GetInlinesHookTests.test_inline_model_admin_has_get_inlines_and_returns_inlines generic_inline_admin.tests_llm.GetInlinesHookTests.test_stackedinline_has_get_inlines_and_returns_inlines generic_inline_admin.tests_llm.GetInlinesHookTests.test_tabularinline_has_get_inlines_and_returns_inlines
coverage json -o coverage.json
: '>>>>> End Test Output'
