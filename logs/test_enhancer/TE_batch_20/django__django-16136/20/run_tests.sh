#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 async.tests_llm.AsyncOnlyView.get async.tests_llm.GetAndPostView.get async.tests_llm.GetAndPostView.post async.tests_llm.RedirectViewTests.setUp async.tests_llm.RedirectViewTests.test_redirectview_appends_query_string_when_enabled async.tests_llm.RedirectViewTests.test_redirectview_returns_temporary_and_permanent_redirects async.tests_llm.SyncOnlyView.get async.tests_llm.ViewBaseTests.setUp async.tests_llm.ViewBaseTests.test_setup_creates_head_when_only_get_defined async.tests_llm._maybe_await
coverage json -o coverage.json
: '>>>>> End Test Output'
