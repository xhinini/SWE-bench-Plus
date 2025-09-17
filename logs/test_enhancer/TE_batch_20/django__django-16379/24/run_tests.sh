#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.FileBasedCacheRegressionTests.setUp cache.tests_llm.FileBasedCacheRegressionTests.tearDown cache.tests_llm.FileBasedCacheRegressionTests.test_has_key_propagates_exceptions_from_is_expired
coverage json -o coverage.json
: '>>>>> End Test Output'
