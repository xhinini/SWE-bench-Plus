#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 messages_tests.test_cookie_llm.CookieTests.test_cookie_update_preserves_empty_extra_tags messages_tests.test_cookie_llm.CookieTests.test_decoder_restores_empty_extra_tags_in_nested_structure messages_tests.test_cookie_llm.CookieTests.test_encoder_excludes_none_extra_tags messages_tests.test_cookie_llm.CookieTests.test_encoder_includes_empty_string_extra_tags messages_tests.test_cookie_llm.CookieTests.test_message_decoder_keeps_safedata_flag_and_extra_tags_empty messages_tests.test_cookie_llm.CookieTests.test_message_serializer_preserves_empty_extra_tags messages_tests.test_cookie_llm.CookieTests.test_nested_list_encoding_with_falsy_extra_tags messages_tests.test_cookie_llm.CookieTests.test_preserve_false_extra_tags messages_tests.test_cookie_llm.CookieTests.test_preserve_zero_extra_tags messages_tests.test_cookie_llm.CookieTests.test_storage_encode_decode_preserves_empty_extra_tags
coverage json -o coverage.json
: '>>>>> End Test Output'
