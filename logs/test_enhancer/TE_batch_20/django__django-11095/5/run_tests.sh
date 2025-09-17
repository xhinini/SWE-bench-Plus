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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.DummyRequest.__init__ generic_inline_admin.tests_llm.GetInlinesRegressionTests.setUp generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_baseclass_get_inlines_available_on_subclass_without_override generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_basemodeladmin_has_get_inlines_and_returns_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_inlinemodeladmin_inherits_get_inlines generic_inline_admin.tests_llm.GetInlinesRegressionTests.test_stacked_and_tabular_inherit_get_inlines generic_inline_admin.tests_llm.MockUser.has_perm
coverage json -o coverage.json
: '>>>>> End Test Output'
