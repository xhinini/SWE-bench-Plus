#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.URLValidatorUnsafeCharsTests.test_class_has_unsafe_chars_attribute validators.tests_llm.URLValidatorUnsafeCharsTests.test_getattr_accessible validators.tests_llm.URLValidatorUnsafeCharsTests.test_instance_has_unsafe_chars_attribute validators.tests_llm.URLValidatorUnsafeCharsTests.test_subclass_can_override_unsafe_chars validators.tests_llm.URLValidatorUnsafeCharsTests.test_subclass_inherits_unsafe_chars validators.tests_llm.URLValidatorUnsafeCharsTests.test_unsafe_chars_contains_tab_cr_lf validators.tests_llm.URLValidatorUnsafeCharsTests.test_unsafe_chars_intersection_detects_forbidden_char validators.tests_llm.URLValidatorUnsafeCharsTests.test_unsafe_chars_is_frozenset validators.tests_llm.URLValidatorUnsafeCharsTests.test_unsafe_chars_shared_between_instances
coverage json -o coverage.json
: '>>>>> End Test Output'
