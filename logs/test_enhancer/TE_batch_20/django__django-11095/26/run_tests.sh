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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.GetInlinesBaseTests._instantiate_generic_tabular generic_inline_admin.tests_llm.GetInlinesBaseTests._instantiate_stacked generic_inline_admin.tests_llm.GetInlinesBaseTests._instantiate_tabular generic_inline_admin.tests_llm.GetInlinesBaseTests.setUp generic_inline_admin.tests_llm.GetInlinesBaseTests.test_base_modeladmin_has_get_inlines generic_inline_admin.tests_llm.GetInlinesBaseTests.test_generic_tabularinline_instance_has_get_inlines_and_returns_inlines generic_inline_admin.tests_llm.GetInlinesBaseTests.test_get_inlines_callable_on_generic_and_tabular generic_inline_admin.tests_llm.GetInlinesBaseTests.test_get_inlines_on_inline_when_inlines_mutated generic_inline_admin.tests_llm.GetInlinesBaseTests.test_inline_class_subclassing_preserves_get_inlines generic_inline_admin.tests_llm.GetInlinesBaseTests.test_inline_get_inlines_accepts_request_and_obj generic_inline_admin.tests_llm.GetInlinesBaseTests.test_multiple_inline_instances_each_have_get_inlines generic_inline_admin.tests_llm.GetInlinesBaseTests.test_stackedinline_instance_has_get_inlines_and_returns_inlines generic_inline_admin.tests_llm.GetInlinesBaseTests.test_tabularinline_instance_has_get_inlines_and_returns_inlines
coverage json -o coverage.json
: '>>>>> End Test Output'
