#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.URLUnsafeCharsTests.setUp validators.tests_llm.URLUnsafeCharsTests.test_subclass_of_str_hiding_contains_still_rejected validators.tests_llm.URLUnsafeCharsTests.test_unsafe_chars_attribute_exists validators.tests_llm.URLUnsafeCharsTests.test_validation_error_message_and_code
coverage json -o coverage.json
: '>>>>> End Test Output'
