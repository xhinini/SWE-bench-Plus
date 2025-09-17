#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.FileBasedCacheRaceTests.test_has_key_does_not_swallow_oserror cache.tests_llm.FileBasedCacheRaceTests.test_has_key_does_not_swallow_permissionerror cache.tests_llm.FileBasedCacheRaceTests.test_has_key_handles_filenotfound_race_default_cache cache.tests_llm.FileBasedCacheRaceTests.test_has_key_handles_filenotfound_race_prefixed_cache cache.tests_llm.FileBasedCacheRaceTests.test_has_key_handles_filenotfound_race_with_version cache.tests_llm.FileBasedCacheRaceTests.test_has_key_handles_filenotfound_when_exists_true cache.tests_llm.FileBasedCacheRaceTests.test_has_key_open_attempt_count cache.tests_llm.FileBasedCacheRaceTests.test_has_key_opens_expected_file_when_race cache.tests_llm.FileBasedCacheRaceTests.test_has_key_race_multiple_calls cache.tests_llm.FileBasedCacheRaceTests.test_in_operator_handles_filenotfound_race
coverage json -o coverage.json
: '>>>>> End Test Output'
