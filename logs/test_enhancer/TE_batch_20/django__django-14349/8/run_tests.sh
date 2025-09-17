#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.CustomUnsafeCharsTests.test_custom_validator_rejects_bang_but_default_allows validators.tests_llm.CustomUnsafeCharsTests.test_default_unsafe_chars_on_class validators.tests_llm.CustomUnsafeCharsTests.test_rejects_bang_in_multiple_positions validators.tests_llm.CustomUnsafeCharsTests.test_rejects_exclamation_in_fragment validators.tests_llm.CustomUnsafeCharsTests.test_rejects_exclamation_in_path validators.tests_llm.CustomUnsafeCharsTests.test_rejects_exclamation_in_query validators.tests_llm.CustomUnsafeCharsTests.test_rejects_exclamation_in_userinfo validators.tests_llm.CustomUnsafeCharsTests.test_rejects_hash_in_fragment_when_overridden
coverage json -o coverage.json
: '>>>>> End Test Output'
