#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.UnsafeCharsTests.test_unsafe_chars_class_attribute_exists validators.tests_llm.UnsafeCharsTests.test_unsafe_chars_contains_expected_characters validators.tests_llm.UnsafeCharsTests.test_unsafe_chars_has_no_add_method validators.tests_llm.UnsafeCharsTests.test_unsafe_chars_instance_attribute_exists validators.tests_llm.UnsafeCharsTests.test_unsafe_chars_intersection_detects_cr validators.tests_llm.UnsafeCharsTests.test_unsafe_chars_intersection_detects_newline validators.tests_llm.UnsafeCharsTests.test_unsafe_chars_intersection_detects_tab validators.tests_llm.UnsafeCharsTests.test_unsafe_chars_is_frozenset validators.tests_llm.UnsafeCharsTests.test_unsafe_chars_repr_contains_frozenset validators.tests_llm.UnsafeCharsTests.test_using_unsafe_chars_to_reject_url
coverage json -o coverage.json
: '>>>>> End Test Output'
