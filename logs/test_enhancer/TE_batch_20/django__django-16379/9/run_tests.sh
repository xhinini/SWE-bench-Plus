#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.test_has_key_empty_file_considered_expired_and_removed cache.tests_llm.test_has_key_false_when_expired cache.tests_llm.test_has_key_handles_open_enoent_race cache.tests_llm.test_has_key_handles_open_enoent_race_with_version cache.tests_llm.test_has_key_no_file_returns_false cache.tests_llm.test_has_key_open_called_once_on_race cache.tests_llm.test_has_key_propagates_other_exceptions cache.tests_llm.test_has_key_propagates_permission_error cache.tests_llm.test_has_key_true_when_not_expired cache.tests_llm.test_has_key_with_versioning
coverage json -o coverage.json
: '>>>>> End Test Output'
