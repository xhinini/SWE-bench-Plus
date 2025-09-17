#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 custom_lookups.tests_llm.TempLookup.as_sql custom_lookups.tests_llm.UnregisterLookupCacheTests._snapshot_and_restore_field_class_lookups custom_lookups.tests_llm.UnregisterLookupCacheTests.test_unregister_clears_cache_when_subclass_cached_before_registration
coverage json -o coverage.json
: '>>>>> End Test Output'
