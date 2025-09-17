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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 generic_inline_admin.tests_llm.BaseGetInlinesTests.test_basemodeladmin_get_inlines_different_types generic_inline_admin.tests_llm.BaseGetInlinesTests.test_basemodeladmin_get_inlines_empty generic_inline_admin.tests_llm.BaseGetInlinesTests.test_basemodeladmin_get_inlines_returns_list generic_inline_admin.tests_llm.BaseGetInlinesTests.test_basemodeladmin_get_inlines_returns_tuple generic_inline_admin.tests_llm.BaseGetInlinesTests.test_basemodeladmin_get_inlines_with_obj generic_inline_admin.tests_llm.DummyMeta.__init__ generic_inline_admin.tests_llm.InlineGetInlinesTests.setUp generic_inline_admin.tests_llm.InlineGetInlinesTests.test_inlinemodeladmin_get_inlines_empty generic_inline_admin.tests_llm.InlineGetInlinesTests.test_inlinemodeladmin_get_inlines_with_obj generic_inline_admin.tests_llm.InlineGetInlinesTests.test_inlinemodeladmin_inherits_get_inlines_list generic_inline_admin.tests_llm.InlineGetInlinesTests.test_inlinemodeladmin_inherits_get_inlines_tuple
coverage json -o coverage.json
: '>>>>> End Test Output'
