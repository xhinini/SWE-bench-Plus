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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_base_model_admin_get_inlines_returns_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_base_model_admin_has_get_inlines_attribute generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inlines_signature_requires_request_and_obj_on_base generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_get_inlines_signature_requires_request_and_obj_on_inline generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_model_admin_get_inlines_returns_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inline_model_admin_has_get_inlines_attribute generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_stackedinline_get_inlines_returns_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_stackedinline_has_get_inlines_attribute generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_tabularinline_get_inlines_returns_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_tabularinline_has_get_inlines_attribute
coverage json -o coverage.json
: '>>>>> End Test Output'
