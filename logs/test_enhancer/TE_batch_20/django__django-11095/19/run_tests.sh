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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.BaseGetInlinesTests.setUp generic_inline_admin.tests_llm.BaseGetInlinesTests.test_inline_get_inlines_accepts_obj_argument generic_inline_admin.tests_llm.BaseGetInlinesTests.test_inline_get_inlines_on_multiple_inline_classes generic_inline_admin.tests_llm.BaseGetInlinesTests.test_inline_get_inlines_respects_class_inlines_attr generic_inline_admin.tests_llm.BaseGetInlinesTests.test_inline_get_inlines_with_request_variations generic_inline_admin.tests_llm.BaseGetInlinesTests.test_inline_model_admin_has_get_inlines_method generic_inline_admin.tests_llm.FakeMeta.__init__ generic_inline_admin.tests_llm.ModelAdminInlineSelectionTests.setUp generic_inline_admin.tests_llm.ModelAdminInlineSelectionTests.test_get_inline_instances_respects_inline_permission_checks generic_inline_admin.tests_llm.ModelAdminInlineSelectionTests.test_modeladmin_get_inline_instances_uses_get_inlines
coverage json -o coverage.json
: '>>>>> End Test Output'
