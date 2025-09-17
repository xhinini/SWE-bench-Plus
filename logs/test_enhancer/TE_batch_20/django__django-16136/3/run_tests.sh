#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 async.tests_llm.AsyncOnlyView.get async.tests_llm.BothAsyncView.get async.tests_llm.BothAsyncView.post async.tests_llm.HttpMethodNotAllowedExtraTests.setUp async.tests_llm.HttpMethodNotAllowedExtraTests.test_dispatch_with_unapproved_verb_uses_http_method_not_allowed_async async.tests_llm.HttpMethodNotAllowedExtraTests.test_dispatch_with_unapproved_verb_uses_http_method_not_allowed_sync async.tests_llm.HttpMethodNotAllowedExtraTests.test_http_method_not_allowed_async_returns_same_response_object_when_awaited async.tests_llm.SyncOnlyView.get
coverage json -o coverage.json
: '>>>>> End Test Output'
