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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.GetInlinesHookTests.setUp generic_inline_admin.tests_llm.GetInlinesHookTests.test_base_modeladmin_has_get_inlines_callable generic_inline_admin.tests_llm.GetInlinesHookTests.test_get_inline_instances_uses_dynamic_get_inlines_based_on_obj generic_inline_admin.tests_llm.GetInlinesHookTests.test_get_inline_instances_with_multiple_inlines_matches_formsets generic_inline_admin.tests_llm.GetInlinesHookTests.test_get_inlines_accepts_tuple_and_generator generic_inline_admin.tests_llm.PermissionInline.has_add_permission generic_inline_admin.tests_llm.PermissionInline.has_change_permission generic_inline_admin.tests_llm.PermissionInline.has_delete_permission generic_inline_admin.tests_llm.PermissionInline.has_view_or_change_permission
coverage json -o coverage.json
: '>>>>> End Test Output'
