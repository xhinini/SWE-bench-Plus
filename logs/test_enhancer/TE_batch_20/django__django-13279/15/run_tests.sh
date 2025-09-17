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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_json_ascii_roundtrip sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_json_with_accented_character sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_json_with_emoji sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_json_with_long_unicode_string sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_json_with_non_ascii_key_and_value sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_pickle_ascii_roundtrip sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_pickle_with_accented_character sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_pickle_with_binary_blob sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_pickle_with_emoji sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_pickle_with_small_binary
coverage json -o coverage.json
: '>>>>> End Test Output'
