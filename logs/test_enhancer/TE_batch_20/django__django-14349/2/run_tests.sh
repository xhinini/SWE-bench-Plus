#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.URLValidatorUnsafeCharsTests.test_space_is_not_considered_unsafe validators.tests_llm.URLValidatorUnsafeCharsTests.test_unsafe_chars_attribute_exists validators.tests_llm.URLValidatorUnsafeCharsTests.test_unsafe_chars_contains_tab_cr_lf validators.tests_llm.URLValidatorUnsafeCharsTests.test_unsafe_chars_is_immutable_frozenset
coverage json -o coverage.json
: '>>>>> End Test Output'
