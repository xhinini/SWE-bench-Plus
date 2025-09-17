#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 custom_lookups.tests_llm.AltLookup.as_sql custom_lookups.tests_llm.AnotherLookup.as_sql custom_lookups.tests_llm.TempLookup.as_sql custom_lookups.tests_llm.UnregisterLookupTests.tearDown custom_lookups.tests_llm.UnregisterLookupTests.test_unregister_on_base_field_affects_derived_fields
coverage json -o coverage.json
: '>>>>> End Test Output'
