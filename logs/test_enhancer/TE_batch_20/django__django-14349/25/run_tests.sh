#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.URLValidatorUnsafeCharsTests.test_has_unsafe_chars_attribute validators.tests_llm.URLValidatorUnsafeCharsTests.test_unsafe_chars_is_frozenset_and_immutable
coverage json -o coverage.json
: '>>>>> End Test Output'
