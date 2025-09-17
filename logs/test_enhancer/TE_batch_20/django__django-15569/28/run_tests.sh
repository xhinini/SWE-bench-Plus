#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 custom_lookups.tests_llm.RegisterLookupMixinUnregisterTests._make_lookup custom_lookups.tests_llm.RegisterLookupMixinUnregisterTests.setUp custom_lookups.tests_llm.RegisterLookupMixinUnregisterTests.tearDown custom_lookups.tests_llm.RegisterLookupMixinUnregisterTests.test_unregistration_raises_keyerror_when_missing
coverage json -o coverage.json
: '>>>>> End Test Output'
