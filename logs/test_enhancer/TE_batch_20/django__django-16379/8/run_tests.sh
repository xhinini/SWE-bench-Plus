#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.FileBasedCacheRaceTests.test_get_open_called_once_on_race cache.tests_llm.FileBasedCacheRaceTests.test_get_os_path_exists_true_and_open_fails_returns_default cache.tests_llm.FileBasedCacheRaceTests.test_get_propagates_oserror cache.tests_llm.FileBasedCacheRaceTests.test_has_key_one_key_races_other_key_ok cache.tests_llm.FileBasedCacheRaceTests.test_has_key_os_path_exists_true_and_open_fails cache.tests_llm.FileBasedCacheRaceTests.test_has_key_propagates_oserror cache.tests_llm.FileBasedCacheRaceTests.test_has_key_transient_race_then_success cache.tests_llm.FileBasedCacheRaceTests.test_has_key_transient_race_then_success_with_specific_target cache.tests_llm.FileBasedCacheRaceTests.test_has_key_unicode_key_open_fails cache.tests_llm.FileBasedCacheRaceTests.test_has_key_version_open_raises_filenotfound
coverage json -o coverage.json
: '>>>>> End Test Output'
