#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 async.tests_llm.AsyncPostOnly.post async.tests_llm.GetOnly.get async.tests_llm.HttpMethodNotAllowedExtraTests.setUp async.tests_llm.HttpMethodNotAllowedExtraTests.test_allowed_methods_includes_head_when_get_defined async.tests_llm.HttpMethodNotAllowedExtraTests.test_empty_view_allowed_methods_is_empty async.tests_llm.OnlyOptionsAsync.options async.tests_llm.SyncGetOnly.get
coverage json -o coverage.json
: '>>>>> End Test Output'
