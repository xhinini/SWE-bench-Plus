#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_inlines.tests_llm.InlineVerboseNamePluralRegressionTests.assert_plural_derived_from_verbose admin_inlines.tests_llm.InlineVerboseNamePluralRegressionTests.test_stacked_person_add_view_heading_uses_derived_plural admin_inlines.tests_llm.InlineVerboseNamePluralRegressionTests.test_tabular_child_add_view_heading_uses_derived_plural
coverage json -o coverage.json
: '>>>>> End Test Output'
