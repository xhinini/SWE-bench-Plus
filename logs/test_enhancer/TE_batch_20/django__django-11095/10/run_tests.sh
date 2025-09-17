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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.FakeModel.__init__ generic_inline_admin.tests_llm.FakeOptions.__init__ generic_inline_admin.tests_llm.GetInlinesTests._make_inline generic_inline_admin.tests_llm.GetInlinesTests.setUp generic_inline_admin.tests_llm.GetInlinesTests.test_get_inline_instances_sets_parent_model_on_inline_instances generic_inline_admin.tests_llm.GetInlinesTests.test_get_inlines_accepts_tuple_and_list generic_inline_admin.tests_llm.GetInlinesTests.test_get_inlines_can_be_request_sensitive generic_inline_admin.tests_llm.GetInlinesTests.test_get_inlines_can_return_empty_iterable generic_inline_admin.tests_llm.GetInlinesTests.test_get_inlines_hook_is_used_to_choose_inlines_based_on_obj generic_inline_admin.tests_llm.GetInlinesTests.test_get_inlines_is_called_with_obj_none_and_obj_instance generic_inline_admin.tests_llm.GetInlinesTests.test_get_inlines_iterable_types_and_order_preserved generic_inline_admin.tests_llm.GetInlinesTests.test_request_truthiness_triggers_permission_checks_and_may_filter_inlines
coverage json -o coverage.json
: '>>>>> End Test Output'
