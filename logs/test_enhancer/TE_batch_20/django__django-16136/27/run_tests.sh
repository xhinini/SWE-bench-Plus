#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 async.tests_llm.GetOnlySyncView.get async.tests_llm.GetPostAsyncView.get async.tests_llm.GetPostAsyncView.post async.tests_llm.HttpMethodNotAllowedRegressionTests.setUp async.tests_llm.HttpMethodNotAllowedRegressionTests.test_allowed_methods_include_defined_methods_async_view async.tests_llm.HttpMethodNotAllowedRegressionTests.test_dispatch_unknown_method_is_coroutine_for_async_view async.tests_llm.HttpMethodNotAllowedRegressionTests.test_dispatch_unknown_method_is_not_coroutine_for_sync_view async.tests_llm.PostOnlyAsyncView.post
coverage json -o coverage.json
: '>>>>> End Test Output'
