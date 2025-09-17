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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_validators_llm.UsernameValidatorRegexTests.test_ascii_regex_does_not_use_capital_a_anchor auth_tests.test_validators_llm.UsernameValidatorRegexTests.test_ascii_regex_starts_with_caret auth_tests.test_validators_llm.UsernameValidatorRegexTests.test_ascii_validator_regex_exact auth_tests.test_validators_llm.UsernameValidatorRegexTests.test_unicode_regex_does_not_use_capital_a_anchor auth_tests.test_validators_llm.UsernameValidatorRegexTests.test_unicode_regex_starts_with_caret auth_tests.test_validators_llm.UsernameValidatorRegexTests.test_unicode_validator_regex_exact
coverage json -o coverage.json
: '>>>>> End Test Output'
