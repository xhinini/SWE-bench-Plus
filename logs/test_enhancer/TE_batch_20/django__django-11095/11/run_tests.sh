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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.BaseGetInlinesTests.test_base_modeladmin_has_get_inlines_and_returns_inlines generic_inline_admin.tests_llm.BaseGetInlinesTests.test_inlinemodeladmin_inherits_get_inlines generic_inline_admin.tests_llm.MockRequest.__init__ generic_inline_admin.tests_llm.MockUser.__init__ generic_inline_admin.tests_llm.MockUser.has_module_perms generic_inline_admin.tests_llm.MockUser.has_perm generic_inline_admin.tests_llm.ModelAdminGetInlineInstancesTests.test_dynamic_get_inlines_based_on_obj_property generic_inline_admin.tests_llm.ModelAdminGetInlineInstancesTests.test_get_inline_instances_uses_get_inlines_override_no_obj generic_inline_admin.tests_llm.ModelAdminGetInlineInstancesTests.test_get_inline_instances_uses_get_inlines_override_with_obj generic_inline_admin.tests_llm.ModelAdminGetInlineInstancesTests.test_get_inlines_respects_tuple_and_list_return_types
coverage json -o coverage.json
: '>>>>> End Test Output'
