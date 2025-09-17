#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_static_llm.WasModifiedSinceInvalidHeaderTests.test_arbitrary_semicolon_pairs view_tests.tests.test_static_llm.WasModifiedSinceInvalidHeaderTests.test_empty_length_assignment view_tests.tests.test_static_llm.WasModifiedSinceInvalidHeaderTests.test_leading_semicolon_with_length view_tests.tests.test_static_llm.WasModifiedSinceInvalidHeaderTests.test_negative_length_value view_tests.tests.test_static_llm.WasModifiedSinceInvalidHeaderTests.test_no_space_after_semicolon_length view_tests.tests.test_static_llm.WasModifiedSinceInvalidHeaderTests.test_non_digit_length_value view_tests.tests.test_static_llm.WasModifiedSinceInvalidHeaderTests.test_trailing_semicolon_only view_tests.tests.test_static_llm.WasModifiedSinceInvalidHeaderTests.test_unrecognized_parameter_after_date
coverage json -o coverage.json
: '>>>>> End Test Output'
