#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_static_llm.WasModifiedSinceAdditionalTests.test_semicolon_with_non_numeric_length view_tests.tests.test_static_llm.WasModifiedSinceAdditionalTests.test_trailing_semicolon_only
coverage json -o coverage.json
: '>>>>> End Test Output'
