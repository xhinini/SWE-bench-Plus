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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodingPickleTests.assert_roundtrip_via_legacy sessions_tests.tests_llm.LegacyEncodingPickleTests.make_session sessions_tests.tests_llm.LegacyEncodingPickleTests.test_decode_uses_legacy_path_and_roundtrips sessions_tests.tests_llm.LegacyEncodingPickleTests.test_large_random_binary_roundtrip sessions_tests.tests_llm.LegacyEncodingPickleTests.test_legacy_encoded_contains_hash_and_serialized_payload sessions_tests.tests_llm.LegacyEncodingPickleTests.test_mixed_bytes_and_strings_roundtrip sessions_tests.tests_llm.LegacyEncodingPickleTests.test_multiple_roundtrips_consistent sessions_tests.tests_llm.LegacyEncodingPickleTests.test_nested_binary_structures_roundtrip sessions_tests.tests_llm.LegacyEncodingPickleTests.test_non_ascii_unicode_in_values_roundtrip sessions_tests.tests_llm.LegacyEncodingPickleTests.test_null_bytes_roundtrip sessions_tests.tests_llm.LegacyEncodingPickleTests.test_simple_binary_value_roundtrip sessions_tests.tests_llm.LegacyEncodingPickleTests.test_tuple_and_mixed_types_roundtrip
coverage json -o coverage.json
: '>>>>> End Test Output'
