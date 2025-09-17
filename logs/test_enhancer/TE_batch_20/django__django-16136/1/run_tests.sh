#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 async.tests_llm.HttpMethodNotAllowedRegressionTests.setUp async.tests_llm.HttpMethodNotAllowedRegressionTests.test_async_as_view_allowed_header_matches_instance_allowed async.tests_llm.LocalAsyncView.get async.tests_llm.LocalSyncView.get
coverage json -o coverage.json
: '>>>>> End Test Output'
