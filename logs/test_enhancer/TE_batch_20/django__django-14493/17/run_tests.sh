#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_storage_llm.TestPostProcessMaxPassesZero._save staticfiles_tests.test_storage_llm.TestPostProcessMaxPassesZero.setUp staticfiles_tests.test_storage_llm.TestPostProcessMaxPassesZero.tearDown staticfiles_tests.test_storage_llm.TestPostProcessMaxPassesZero.test_stored_name_with_zero_max_passes_caches_value
coverage json -o coverage.json
: '>>>>> End Test Output'
