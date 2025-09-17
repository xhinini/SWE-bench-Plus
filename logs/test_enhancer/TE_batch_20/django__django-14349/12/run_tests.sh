#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.URLValidatorUnsafeCharsTests.test_instance_unsafe_chars_supports_string_assignment validators.tests_llm.URLValidatorUnsafeCharsTests.test_subclass_unsafe_chars_blocks_custom_char validators.tests_llm.URLValidatorUnsafeCharsTests.test_subclass_unsafe_chars_combination
coverage json -o coverage.json
: '>>>>> End Test Output'
