#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 messages_tests.test_cookie_llm.test_cookiestorage_encode_decode_empty_extra_tags messages_tests.test_cookie_llm.test_decoder_nested_empty_extra_tags messages_tests.test_cookie_llm.test_encoder_excludes_none_extra_tags_direct messages_tests.test_cookie_llm.test_encoder_includes_empty_extra_tags_direct messages_tests.test_cookie_llm.test_encoder_includes_zero_extra_tags_value messages_tests.test_cookie_llm.test_json_array_length_for_various_extra_tags messages_tests.test_cookie_llm.test_serializer_roundtrip_empty_extra_tags messages_tests.test_cookie_llm.test_set_cookie_helper_preserves_empty_extra_tags messages_tests.test_cookie_llm.test_signed_cookie_preserves_empty_extra_tags_via_get messages_tests.test_cookie_llm.test_update_sets_cookie_preserving_empty_extra_tags
coverage json -o coverage.json
: '>>>>> End Test Output'
