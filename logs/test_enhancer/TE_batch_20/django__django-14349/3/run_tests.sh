#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.URLUnsafeCharsTests.test_carriage_return_detected_and_rejected validators.tests_llm.URLUnsafeCharsTests.test_newline_after_ipv6_host_rejected validators.tests_llm.URLUnsafeCharsTests.test_newline_at_start_rejected validators.tests_llm.URLUnsafeCharsTests.test_newline_detected_and_rejected validators.tests_llm.URLUnsafeCharsTests.test_newline_in_scheme_rejected validators.tests_llm.URLUnsafeCharsTests.test_newline_in_userinfo_rejected validators.tests_llm.URLUnsafeCharsTests.test_tab_detected_and_rejected validators.tests_llm.URLUnsafeCharsTests.test_unsafe_chars_class_attribute validators.tests_llm.URLUnsafeCharsTests.test_unsafe_chars_instance_attribute
coverage json -o coverage.json
: '>>>>> End Test Output'
