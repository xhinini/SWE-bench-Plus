#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.FileBasedCacheRaceTests.test_has_key_handles_race_between_exists_and_open cache.tests_llm.FileBasedCacheRaceTests.test_has_key_handles_race_when_open_raises_filenotfound_multiple_calls cache.tests_llm.FileBasedCacheRaceTests.test_has_key_handles_race_with_unicode_key cache.tests_llm.FileBasedCacheRaceTests.test_has_key_handles_race_with_version cache.tests_llm.FileBasedCacheRaceTests.test_has_key_open_called_with_expected_filename_for_version cache.tests_llm.FileBasedCacheRaceTests.test_has_key_open_called_with_expected_filename_on_race cache.tests_llm.FileBasedCacheRaceTests.test_has_key_propagates_OSError_not_FileNotFoundError cache.tests_llm.FileBasedCacheRaceTests.test_has_key_propagates_PermissionError cache.tests_llm.FileBasedCacheRaceTests.test_has_key_returns_false_for_empty_cache_file
coverage json -o coverage.json
: '>>>>> End Test Output'
