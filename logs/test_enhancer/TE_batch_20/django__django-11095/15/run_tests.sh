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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.BaseGetInlinesTests.test_base_model_admin_get_inlines_accepts_single_arg generic_inline_admin.tests_llm.BaseGetInlinesTests.test_base_model_admin_get_inlines_with_obj generic_inline_admin.tests_llm.DummyAdminSite.is_registered generic_inline_admin.tests_llm.GetInlineInstancesBehaviorTests.test_get_inline_instances_includes_when_request_falsy generic_inline_admin.tests_llm.GetInlineInstancesBehaviorTests.test_get_inline_instances_respects_permissions_with_request generic_inline_admin.tests_llm.GetInlineInstancesBehaviorTests.test_get_inline_instances_uses_get_inlines_and_obj generic_inline_admin.tests_llm.InlineGetInlinesTests.test_inline_model_admin_get_inlines_accepts_single_arg generic_inline_admin.tests_llm.InlineGetInlinesTests.test_inline_model_admin_get_inlines_with_obj
coverage json -o coverage.json
: '>>>>> End Test Output'
