#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.FileBasedHasKeyRaceTests.setUp cache.tests_llm.FileBasedHasKeyRaceTests.tearDown cache.tests_llm.FileBasedHasKeyRaceTests.test_has_key_handles_race_when_file_disappears cache.tests_llm.FileBasedHasKeyRaceTests.test_has_key_multiple_consecutive_race_calls cache.tests_llm.FileBasedHasKeyRaceTests.test_has_key_propagates_other_exceptions cache.tests_llm.FileBasedHasKeyRaceTests.test_has_key_race_does_not_remove_cache_dir cache.tests_llm.FileBasedHasKeyRaceTests.test_has_key_with_spaces_and_unicode_handles_race
coverage json -o coverage.json
: '>>>>> End Test Output'
