#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 messages_tests.test_cookie_llm.CookieExtraTagsTests.get_request messages_tests.test_cookie_llm.CookieExtraTagsTests.get_response messages_tests.test_cookie_llm.CookieExtraTagsTests.get_storage messages_tests.test_cookie_llm.CookieExtraTagsTests.setUp messages_tests.test_cookie_llm.CookieExtraTagsTests.test_store_trimming_preserves_empty_extra_tags
coverage json -o coverage.json
: '>>>>> End Test Output'
