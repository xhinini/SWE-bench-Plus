#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_static_llm.WasModifiedSinceRegressionTests.test_length_with_non_digit_value_after_valid_date_returns_true view_tests.tests.test_static_llm.WasModifiedSinceRegressionTests.test_semicolon_length_no_digits_returns_true view_tests.tests.test_static_llm.WasModifiedSinceRegressionTests.test_semicolon_length_only_returns_true view_tests.tests.test_static_llm.WasModifiedSinceRegressionTests.test_semicolon_no_space_length_returns_true
coverage json -o coverage.json
: '>>>>> End Test Output'
