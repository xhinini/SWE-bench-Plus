#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.URLValidatorUnsafeCharsTests.test_class_level_override_of_unsafe_chars_affects_validation validators.tests_llm.URLValidatorUnsafeCharsTests.test_instance_subclass_override_of_unsafe_chars_affects_validation validators.tests_llm.URLValidatorUnsafeCharsTests.test_modifying_class_attribute_restored_properly_between_tests validators.tests_llm.URLValidatorUnsafeCharsTests.test_unsafe_chars_attribute_exists_and_default
coverage json -o coverage.json
: '>>>>> End Test Output'
