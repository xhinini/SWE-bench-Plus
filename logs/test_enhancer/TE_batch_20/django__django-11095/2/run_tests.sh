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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.FakeInlineClass.__init__ generic_inline_admin.tests_llm.FakeInlineClass.has_add_permission generic_inline_admin.tests_llm.FakeInlineClass.has_delete_permission generic_inline_admin.tests_llm.FakeInlineClass.has_view_or_change_permission generic_inline_admin.tests_llm.GetInlinesTests.setUp generic_inline_admin.tests_llm.GetInlinesTests.test_base_modeladmin_has_get_inlines generic_inline_admin.tests_llm.GetInlinesTests.test_inlinemodeladmin_has_get_inlines generic_inline_admin.tests_llm.MockUser.has_perm
coverage json -o coverage.json
: '>>>>> End Test Output'
