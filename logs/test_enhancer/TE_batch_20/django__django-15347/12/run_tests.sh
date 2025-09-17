#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 messages_tests.test_cookie_llm.test_encode_decode_multiple_messages_mixed_extra_tags messages_tests.test_cookie_llm.test_encoder_preserves_empty_list_extra_tags messages_tests.test_cookie_llm.test_encoder_preserves_empty_string_in_nested_structure messages_tests.test_cookie_llm.test_encoder_preserves_false_extra_tags messages_tests.test_cookie_llm.test_encoder_preserves_zero_extra_tags messages_tests.test_cookie_llm.test_encoder_preserves_zero_in_nested_structure messages_tests.test_cookie_llm.test_serializer_roundtrip_empty_string_extra_tags messages_tests.test_cookie_llm.test_serializer_roundtrip_false_extra_tags messages_tests.test_cookie_llm.test_storage_encode_decode_empty_string_extra_tags messages_tests.test_cookie_llm.test_storage_encode_decode_false_extra_tags
coverage json -o coverage.json
: '>>>>> End Test Output'
