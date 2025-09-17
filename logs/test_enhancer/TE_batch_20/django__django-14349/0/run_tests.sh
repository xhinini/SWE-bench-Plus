#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.URLValidatorUnsafeCharsTests.test_custom_unsafe_digit_in_path validators.tests_llm.URLValidatorUnsafeCharsTests.test_custom_unsafe_in_query_with_instance_override validators.tests_llm.URLValidatorUnsafeCharsTests.test_instance_custom_unsafe_in_userinfo validators.tests_llm.URLValidatorUnsafeCharsTests.test_instance_override_respected_for_path validators.tests_llm.URLValidatorUnsafeCharsTests.test_multiple_custom_unsafe_chars validators.tests_llm.URLValidatorUnsafeCharsTests.test_subclass_custom_unsafe_in_fragment validators.tests_llm.URLValidatorUnsafeCharsTests.test_subclass_custom_unsafe_in_path validators.tests_llm.URLValidatorUnsafeCharsTests.test_subclass_custom_unsafe_in_query validators.tests_llm.URLValidatorUnsafeCharsTests.test_subclass_custom_unsafe_in_userinfo validators.tests_llm.URLValidatorUnsafeCharsTests.test_unicode_custom_unsafe_char
coverage json -o coverage.json
: '>>>>> End Test Output'
