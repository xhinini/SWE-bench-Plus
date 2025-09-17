#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 custom_lookups.tests_llm.RegisterLookupUnregisterTests.setUp custom_lookups.tests_llm.RegisterLookupUnregisterTests.tearDown custom_lookups.tests_llm.RegisterLookupUnregisterTests.test_unregister_with_instance custom_lookups.tests_llm.TempLookupA.as_sql custom_lookups.tests_llm.TempLookupB.as_sql
coverage json -o coverage.json
: '>>>>> End Test Output'
