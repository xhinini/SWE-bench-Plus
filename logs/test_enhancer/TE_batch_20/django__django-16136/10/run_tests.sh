#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 async.tests_llm.AsyncOnlyGet.get async.tests_llm.AsyncOnlyPost.post async.tests_llm.HttpMethodNotAllowedAndOptionsTests.setUp async.tests_llm.SyncOnlyGet.get async.tests_llm.SyncOnlyPost.post
coverage json -o coverage.json
: '>>>>> End Test Output'
