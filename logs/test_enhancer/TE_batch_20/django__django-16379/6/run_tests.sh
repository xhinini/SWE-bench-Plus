#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.test_has_key_called_with_correct_filename cache.tests_llm.test_has_key_does_not_swallow_other_exceptions cache.tests_llm.test_has_key_propagates_os_error cache.tests_llm.test_has_key_race_handling_multiple_calls cache.tests_llm.test_has_key_race_handling_versioned cache.tests_llm.test_has_key_unicode_key_race_handling cache.tests_llm.test_in_operator_race_handling_for_filebased cache.tests_llm.test_prefix_cache_has_key_race_handling cache.tests_llm.test_v2_cache_has_key_race_handling
coverage json -o coverage.json
: '>>>>> End Test Output'
