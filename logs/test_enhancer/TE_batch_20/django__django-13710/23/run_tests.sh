#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_inlines.tests_llm.TestInlineVerboseNamePluralLazy.test_format_lazy_verbose_name_results_in_lazy_plural admin_inlines.tests_llm.TestInlineVerboseNamePluralLazy.test_stacked_gettext_lazy_verbose_name_results_in_lazy_plural admin_inlines.tests_llm.TestInlineVerboseNamePluralLazy.test_stacked_plain_string_verbose_name_results_in_lazy_plural admin_inlines.tests_llm.TestInlineVerboseNamePluralLazy.test_tabular_gettext_lazy_verbose_name_results_in_lazy_plural admin_inlines.tests_llm.TestInlineVerboseNamePluralLazy.test_tabular_plain_string_verbose_name_results_in_lazy_plural admin_inlines.tests_llm.TestInlineVerboseNamePluralLazy.test_verbose_name_on_different_model_preserves_lazy_plural
coverage json -o coverage.json
: '>>>>> End Test Output'
