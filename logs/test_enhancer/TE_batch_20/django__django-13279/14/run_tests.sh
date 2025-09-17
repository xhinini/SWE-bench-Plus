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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodeTests.test_decode_handles_legacy_when_current_algo_changed sessions_tests.tests_llm.LegacyEncodeTests.test_json_legacy_encode_no_attribute_error sessions_tests.tests_llm.LegacyEncodeTests.test_json_legacy_encode_roundtrip_via__legacy_decode sessions_tests.tests_llm.LegacyEncodeTests.test_json_legacy_encode_roundtrip_via_decode sessions_tests.tests_llm.LegacyEncodeTests.test_json_legacy_encoded_contains_colon_separator sessions_tests.tests_llm.LegacyEncodeTests.test_json_legacy_handles_unicode_payload sessions_tests.tests_llm.LegacyEncodeTests.test_legacy_encode_with_larger_payload sessions_tests.tests_llm.LegacyEncodeTests.test_pickle_legacy_encode_roundtrip_via__legacy_decode sessions_tests.tests_llm.LegacyEncodeTests.test_pickle_legacy_encode_roundtrip_via_decode sessions_tests.tests_llm.LegacyEncodeTests.test_pickle_with_bytes_value_roundtrip
coverage json -o coverage.json
: '>>>>> End Test Output'
