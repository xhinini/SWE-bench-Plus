#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 async.tests_llm.BadSetupView.setup async.tests_llm.GetPostView.get async.tests_llm.GetPostView.post async.tests_llm.OnlyGetView.get async.tests_llm.PostOnlyAsyncView.post async.tests_llm.PostOnlySyncView.post async.tests_llm.ViewHttpMethodNotAllowedTests.setUp async.tests_llm.ViewHttpMethodNotAllowedTests.test_allowed_methods_empty_view_and_405_response async.tests_llm.ViewHttpMethodNotAllowedTests.test_allowed_methods_reflects_defined_handlers async.tests_llm.ViewHttpMethodNotAllowedTests.test_setup_assigns_head_when_missing
coverage json -o coverage.json
: '>>>>> End Test Output'
