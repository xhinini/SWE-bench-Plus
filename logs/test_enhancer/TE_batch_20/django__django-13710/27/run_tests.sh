#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_inlines.tests_llm.TestInlineVerboseNamePlural.make_inline admin_inlines.tests_llm.TestInlineVerboseNamePlural.test_person_verbose_name_lazy_preserves_lazy_plural_type admin_inlines.tests_llm.TestInlineVerboseNamePlural.test_profile_verbose_name_lazy_preserved
coverage json -o coverage.json
: '>>>>> End Test Output'
