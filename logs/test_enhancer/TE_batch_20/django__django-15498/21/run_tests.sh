#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_static_llm.WasModifiedSinceRegressionTests.test_header_with_trailing_whitespace_and_length_handled view_tests.tests.test_static_llm.WasModifiedSinceRegressionTests.test_malformed_header_empty_length_value view_tests.tests.test_static_llm.WasModifiedSinceRegressionTests.test_malformed_header_non_digit_length view_tests.tests.test_static_llm.WasModifiedSinceRegressionTests.test_malformed_header_only_length_param
coverage json -o coverage.json
: '>>>>> End Test Output'
