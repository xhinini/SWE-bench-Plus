#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.URLUnsafeCharsTests.test_class_override_applies_to_new_instances validators.tests_llm.URLUnsafeCharsTests.test_class_override_blocks_char_in_path validators.tests_llm.URLUnsafeCharsTests.test_instance_has_unsafe_chars_attribute_even_for_non_str_input validators.tests_llm.URLUnsafeCharsTests.test_instance_override_blocks_char_in_path validators.tests_llm.URLUnsafeCharsTests.test_instance_override_precedence_over_class validators.tests_llm.URLUnsafeCharsTests.test_modifying_unsafe_chars_restored validators.tests_llm.URLUnsafeCharsTests.test_setting_unsafe_chars_to_multiple_chars validators.tests_llm.URLUnsafeCharsTests.test_unsafe_chars_attribute_exists validators.tests_llm.URLUnsafeCharsTests.test_unsafe_chars_default_contents validators.tests_llm.URLUnsafeCharsTests.test_unsafe_chars_is_frozenset_type
coverage json -o coverage.json
: '>>>>> End Test Output'
