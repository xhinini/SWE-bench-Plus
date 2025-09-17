#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm._ensure_and_run_startapp admin_scripts.tests_llm.test_target_absolute_with_trailing_dot admin_scripts.tests_llm.test_target_dot_in_middle_with_trailing_dot admin_scripts.tests_llm.test_target_dotdot_interior_and_trailing_dot admin_scripts.tests_llm.test_target_redundant_slashes_and_dot admin_scripts.tests_llm.test_target_repeated_dot_segments admin_scripts.tests_llm.test_target_trailing_dot admin_scripts.tests_llm.test_target_trailing_dot_slash admin_scripts.tests_llm.test_target_trailing_dotdot admin_scripts.tests_llm.test_target_trailing_dotdot_with_slash
coverage json -o coverage.json
: '>>>>> End Test Output'
