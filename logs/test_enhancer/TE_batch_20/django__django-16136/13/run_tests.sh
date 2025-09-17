#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 async.tests_llm.AsyncOnlyView.get async.tests_llm.GenericBaseTests.setUp async.tests_llm.GenericBaseTests.test_redirect_view_preserves_query_string_when_requested async.tests_llm.OnlyPostAsyncView.post async.tests_llm.SetupBrokenView.setup async.tests_llm.SyncOnlyView.get
coverage json -o coverage.json
: '>>>>> End Test Output'
