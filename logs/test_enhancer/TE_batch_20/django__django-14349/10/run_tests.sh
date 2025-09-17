#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.UnsafeCharsTests.test_custom_unsafe_char_rejected_in_fragment validators.tests_llm.UnsafeCharsTests.test_custom_unsafe_char_rejected_in_password validators.tests_llm.UnsafeCharsTests.test_custom_unsafe_char_rejected_in_path validators.tests_llm.UnsafeCharsTests.test_custom_unsafe_char_rejected_in_query validators.tests_llm.UnsafeCharsTests.test_custom_unsafe_char_rejected_in_username validators.tests_llm.UnsafeCharsTests.test_mutating_unsafe_chars_on_class_affects_instances validators.tests_llm.UnsafeCharsTests.test_setting_instance_unsafe_chars_does_not_affect_other_instances validators.tests_llm.UnsafeCharsTests.test_subclass_with_empty_unsafe_chars_allows_exclamation validators.tests_llm.UnsafeCharsTests.test_subclass_with_unsafe_chars_rejects_exclamation validators.tests_llm.UnsafeCharsTests.test_urlvalidator_has_unsafe_chars_attribute
coverage json -o coverage.json
: '>>>>> End Test Output'
