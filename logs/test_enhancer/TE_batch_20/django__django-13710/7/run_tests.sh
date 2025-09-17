#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_inlines.tests_llm.InlineVerboseNamePluralLazyTests.test_inlinemodeladmin_lazy_verbose_name_produces_lazy_plural admin_inlines.tests_llm.InlineVerboseNamePluralLazyTests.test_lazy_plural_for_different_model_stacked admin_inlines.tests_llm.InlineVerboseNamePluralLazyTests.test_lazy_plural_for_different_model_tabular admin_inlines.tests_llm.InlineVerboseNamePluralLazyTests.test_lazy_verbose_name_with_unicode_characters admin_inlines.tests_llm.InlineVerboseNamePluralLazyTests.test_stackedinline_lazy_verbose_name_produces_lazy_plural admin_inlines.tests_llm.InlineVerboseNamePluralLazyTests.test_tabularinline_lazy_verbose_name_produces_lazy_plural
coverage json -o coverage.json
: '>>>>> End Test Output'
