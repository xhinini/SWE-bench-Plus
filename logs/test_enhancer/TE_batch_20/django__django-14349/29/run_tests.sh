#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.CustomUnsafeCharsTests.test_instance_unsafe_chars_blocks_dollar validators.tests_llm.CustomUnsafeCharsTests.test_multiple_unsafe_chars_blocks_percent_and_caret validators.tests_llm.CustomUnsafeCharsTests.test_subclass_combines_defaults_and_adds_plus validators.tests_llm.CustomUnsafeCharsTests.test_subclass_unsafe_chars_blocks_plus validators.tests_llm.CustomUnsafeCharsTests.test_unicode_unsafe_char_blocks_checkmark validators.tests_llm.CustomUnsafeCharsTests.test_unsafe_char_in_netloc_blocks_hyphen validators.tests_llm.CustomUnsafeCharsTests.test_unsafe_char_in_password_blocks_dollar validators.tests_llm.CustomUnsafeCharsTests.test_unsafe_char_in_query_blocks_plus validators.tests_llm.CustomUnsafeCharsTests.test_unsafe_char_in_userinfo_blocks_plus
coverage json -o coverage.json
: '>>>>> End Test Output'
