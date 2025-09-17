#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_inlines.tests_llm.TestInlineVerboseNamePluralRegression.test_lazy_verbose_name_uses_derived_plural_not_model_meta admin_inlines.tests_llm.TestInlineVerboseNamePluralRegression.test_plain_verbose_name_uses_derived_plural_not_model_meta
coverage json -o coverage.json
: '>>>>> End Test Output'
