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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodingTests.test_encode_does_not_raise_unicode_error_json sessions_tests.tests_llm.LegacyEncodingTests.test_encode_does_not_raise_unicode_error_pickle sessions_tests.tests_llm.LegacyEncodingTests.test_legacy_encode_and_decode_roundtrip_after_switch_algo_json sessions_tests.tests_llm.LegacyEncodingTests.test_legacy_encode_non_ascii_json_cafe sessions_tests.tests_llm.LegacyEncodingTests.test_legacy_encode_non_ascii_json_emoji sessions_tests.tests_llm.LegacyEncodingTests.test_legacy_encode_non_ascii_pickle_cafe sessions_tests.tests_llm.LegacyEncodingTests.test_legacy_encode_non_ascii_pickle_emoji sessions_tests.tests_llm.LegacyEncodingTests.test_legacy_encoded_base64_contains_colon_separator_json sessions_tests.tests_llm.LegacyEncodingTests.test_multiple_non_ascii_fields_roundtrip
coverage json -o coverage.json
: '>>>>> End Test Output'
