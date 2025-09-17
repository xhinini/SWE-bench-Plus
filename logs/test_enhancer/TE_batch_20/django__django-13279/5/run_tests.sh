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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodeTests.tearDown sessions_tests.tests_llm.LegacyEncodeTests.test_legacy_encode_binary_value_with_pickle sessions_tests.tests_llm.LegacyEncodeTests.test_legacy_encode_decode_roundtrip_via_decode sessions_tests.tests_llm.LegacyEncodeTests.test_legacy_encode_does_not_raise_on_str_serialized sessions_tests.tests_llm.LegacyEncodeTests.test_legacy_encode_empty_dict sessions_tests.tests_llm.LegacyEncodeTests.test_legacy_encode_handles_non_ascii_json sessions_tests.tests_llm.LegacyEncodeTests.test_legacy_encode_json_compatible_with_legacy_decode sessions_tests.tests_llm.LegacyEncodeTests.test_legacy_encode_longer_serialized_content sessions_tests.tests_llm.LegacyEncodeTests.test_legacy_encode_nested_structures sessions_tests.tests_llm.LegacyEncodeTests.test_legacy_encode_pickle_roundtrip sessions_tests.tests_llm.LegacyEncodeTests.test_legacy_encoded_starts_with_hash_and_colon
coverage json -o coverage.json
: '>>>>> End Test Output'
