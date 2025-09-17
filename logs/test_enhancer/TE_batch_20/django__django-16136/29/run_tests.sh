#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 async.tests_llm.AdditionalHttpMethodNotAllowedTests.setUp async.tests_llm.AsyncOnlyPostView.post async.tests_llm.AsyncView.get async.tests_llm.SyncView.get
coverage json -o coverage.json
: '>>>>> End Test Output'
