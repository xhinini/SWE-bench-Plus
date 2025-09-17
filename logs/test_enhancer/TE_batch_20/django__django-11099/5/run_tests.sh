#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_validators_llm.AdditionalUsernameValidatorsTests.test_ascii_accepts_allowed_characters_and_rejects_unicode_letters auth_tests.test_validators_llm.AdditionalUsernameValidatorsTests.test_ascii_rejects_trailing_newline auth_tests.test_validators_llm.AdditionalUsernameValidatorsTests.test_ascii_rejects_various_line_separators auth_tests.test_validators_llm.AdditionalUsernameValidatorsTests.test_regex_string_is_expected_for_ascii auth_tests.test_validators_llm.AdditionalUsernameValidatorsTests.test_regex_string_is_expected_for_unicode auth_tests.test_validators_llm.AdditionalUsernameValidatorsTests.test_unicode_accepts_unicode_letters auth_tests.test_validators_llm.AdditionalUsernameValidatorsTests.test_unicode_rejects_trailing_newline auth_tests.test_validators_llm.AdditionalUsernameValidatorsTests.test_unicode_rejects_various_line_separators auth_tests.test_validators_llm.AdditionalUsernameValidatorsTests.test_validation_error_message_matches_validator_message_ascii auth_tests.test_validators_llm.AdditionalUsernameValidatorsTests.test_validation_error_message_matches_validator_message_unicode
coverage json -o coverage.json
: '>>>>> End Test Output'
