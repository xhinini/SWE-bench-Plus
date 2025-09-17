#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 async.tests_llm.AsyncOnlyView.get async.tests_llm.HttpMethodNotAllowedRegressionTests.setUp async.tests_llm.HttpMethodNotAllowedRegressionTests.test_allowed_methods_list_reflects_declared_handlers_without_setup async.tests_llm.HttpMethodNotAllowedRegressionTests.test_dispatch_via_as_view_unknown_verb_async async.tests_llm.HttpMethodNotAllowedRegressionTests.test_unknown_http_verb_treated_as_not_allowed_async async.tests_llm.SyncOnlyView.get
coverage json -o coverage.json
: '>>>>> End Test Output'
