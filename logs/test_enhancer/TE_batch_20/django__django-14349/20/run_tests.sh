#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.URLValidatorUnsafeCharsTests.test_class_override_rejects_percent_in_fragment validators.tests_llm.URLValidatorUnsafeCharsTests.test_instance_override_rejects_at_in_userinfo validators.tests_llm.URLValidatorUnsafeCharsTests.test_instance_override_rejects_dollar_in_path validators.tests_llm.URLValidatorUnsafeCharsTests.test_multiple_chars_in_unsafe_chars validators.tests_llm.URLValidatorUnsafeCharsTests.test_setting_unsafe_chars_affects_new_instances validators.tests_llm.URLValidatorUnsafeCharsTests.test_subclass_custom_unsafe_chars_rejects_multiple validators.tests_llm.URLValidatorUnsafeCharsTests.test_subclass_override_rejects_hash_in_fragment validators.tests_llm.URLValidatorUnsafeCharsTests.test_unsafe_chars_attribute_present validators.tests_llm.URLValidatorUnsafeCharsTests.test_unsafe_chars_is_frozenset_and_default_members
coverage json -o coverage.json
: '>>>>> End Test Output'
