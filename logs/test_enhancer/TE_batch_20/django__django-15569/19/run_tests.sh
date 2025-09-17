#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 custom_lookups.tests_llm.UnregisterLookupCacheTests._restore_class_lookups custom_lookups.tests_llm.UnregisterLookupCacheTests._save_and_clear_class_lookups custom_lookups.tests_llm.UnregisterLookupCacheTests.setUp custom_lookups.tests_llm.make_lookup
coverage json -o coverage.json
: '>>>>> End Test Output'
