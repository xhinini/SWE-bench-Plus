#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.test_has_key_called_once_when_open_raises_FileNotFoundError cache.tests_llm.test_has_key_does_not_propagate_FileNotFoundError_on_pathlib_location cache.tests_llm.test_has_key_in_operator_with_prefixed_cache_handles_race cache.tests_llm.test_has_key_race_for_prefixed_cache cache.tests_llm.test_has_key_race_for_v2_cache_default_version cache.tests_llm.test_has_key_race_handles_unicode_key cache.tests_llm.test_has_key_race_os_path_exists_true_open_raises cache.tests_llm.test_has_key_race_with_version_argument cache.tests_llm.test_has_key_with_version_and_prefix_combination_race cache.tests_llm.test_in_operator_uses_has_key_and_handles_race
coverage json -o coverage.json
: '>>>>> End Test Output'
