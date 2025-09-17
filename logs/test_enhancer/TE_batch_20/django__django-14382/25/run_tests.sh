#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.test_valid_absolute_target_with_parent_ref admin_scripts.tests_llm.test_valid_absolute_target_with_parent_ref_trailing_slash admin_scripts.tests_llm.test_valid_target_with_dot_segment admin_scripts.tests_llm.test_valid_target_with_double_slashes_and_parent_ref admin_scripts.tests_llm.test_valid_target_with_leading_dot admin_scripts.tests_llm.test_valid_target_with_nested_parent_ref admin_scripts.tests_llm.test_valid_target_with_parent_and_current_dir_combination admin_scripts.tests_llm.test_valid_target_with_parent_ref admin_scripts.tests_llm.test_valid_target_with_parent_ref_trailing_slash
coverage json -o coverage.json
: '>>>>> End Test Output'
