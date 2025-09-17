#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 async.tests_llm.AsyncViewForTests.get async.tests_llm.NewGenericBaseTests._resolve_response async.tests_llm.NewGenericBaseTests.setUp async.tests_llm.NewGenericBaseTests.test_redirect_view_head_and_post_delegate_to_get_and_return_proper_response async.tests_llm.SyncViewForTests.get
coverage json -o coverage.json
: '>>>>> End Test Output'
