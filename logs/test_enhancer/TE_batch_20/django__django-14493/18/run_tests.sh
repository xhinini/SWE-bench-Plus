#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_storage_llm.TestPostProcessMaxPassesZero._run_post_process staticfiles_tests.test_storage_llm.TestPostProcessMaxPassesZero._write staticfiles_tests.test_storage_llm.TestPostProcessMaxPassesZero.setUp staticfiles_tests.test_storage_llm.TestPostProcessMaxPassesZero.tearDown staticfiles_tests.test_storage_llm.TestPostProcessMaxPassesZero.test_zero_pass_path_ending_with_slash
coverage json -o coverage.json
: '>>>>> End Test Output'
