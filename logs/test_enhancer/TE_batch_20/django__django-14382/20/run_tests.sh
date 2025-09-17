#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.StartAppPathNormalization._prepare_app_dir admin_scripts.tests_llm.StartAppPathNormalization.test_dot_with_prefix admin_scripts.tests_llm.StartAppPathNormalization.test_dot_with_prefix_slash admin_scripts.tests_llm.StartAppPathNormalization.test_double_slash_and_dot admin_scripts.tests_llm.StartAppPathNormalization.test_multiple_dot_segments admin_scripts.tests_llm.StartAppPathNormalization.test_parent_with_prefix admin_scripts.tests_llm.StartAppPathNormalization.test_parent_with_prefix_slash admin_scripts.tests_llm.StartAppPathNormalization.test_trailing_dot_in_target_app_directory_name admin_scripts.tests_llm.StartAppPathNormalization.test_trailing_dot_slash_in_target_app_directory_name admin_scripts.tests_llm.StartAppPathNormalization.test_trailing_parent_in_target_app_directory_name admin_scripts.tests_llm.StartAppPathNormalization.test_trailing_parent_slash_in_target_app_directory_name
coverage json -o coverage.json
: '>>>>> End Test Output'
