#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 async.tests_llm.AsyncGetOnly.get async.tests_llm.AsyncGetPost.get async.tests_llm.AsyncGetPost.post async.tests_llm.AsyncHeadDefined.head async.tests_llm.AsyncPostOnly.post async.tests_llm.HttpMethodNotAllowedAsyncTests.setUp async.tests_llm.HttpMethodNotAllowedAsyncTests.test_allowed_methods_header_on_http_method_not_allowed_async_view_contains_methods_uppercase async.tests_llm.HttpMethodNotAllowedAsyncTests.test_http_method_not_allowed_awaitable_contains_allow_header_for_async_view async.tests_llm.OptionsOnly.options
coverage json -o coverage.json
: '>>>>> End Test Output'
