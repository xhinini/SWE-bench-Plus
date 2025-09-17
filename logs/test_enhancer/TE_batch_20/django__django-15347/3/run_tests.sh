#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 messages_tests.test_cookie_llm.ExtraTagsRegressionTests.test_cookie_storage_preserves_empty_string_extra_tags messages_tests.test_cookie_llm.ExtraTagsRegressionTests.test_cookie_storage_preserves_false_extra_tags
coverage json -o coverage.json
: '>>>>> End Test Output'
