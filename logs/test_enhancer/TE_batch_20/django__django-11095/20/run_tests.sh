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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.GetInlinesAPITest.test_base_model_admin_has_get_inlines generic_inline_admin.tests_llm.GetInlinesAPITest.test_get_inlines_is_callable_on_class_and_instance generic_inline_admin.tests_llm.GetInlinesAPITest.test_get_inlines_presence_implies_override_point generic_inline_admin.tests_llm.GetInlinesAPITest.test_get_inlines_signature_has_obj_default generic_inline_admin.tests_llm.GetInlinesAPITest.test_inline_model_admin_has_get_inlines generic_inline_admin.tests_llm.GetInlinesAPITest.test_stackedinline_has_get_inlines generic_inline_admin.tests_llm.GetInlinesAPITest.test_tabularinline_has_get_inlines
coverage json -o coverage.json
: '>>>>> End Test Output'
