#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.test_has_key_does_not_create_file cache.tests_llm.test_has_key_expired_file_deleted cache.tests_llm.test_has_key_is_expired_raising_filenotfound_is_handled cache.tests_llm.test_has_key_is_expired_raising_other_errors_propagates cache.tests_llm.test_has_key_missing_file_returns_false cache.tests_llm.test_has_key_open_raises_filenotfound cache.tests_llm.test_has_key_open_raises_oserror_propagates cache.tests_llm.test_has_key_unexpired_true cache.tests_llm.test_has_key_uses_expected_filename_when_opening cache.tests_llm.test_has_key_with_version_handles_filenotfound
coverage json -o coverage.json
: '>>>>> End Test Output'
