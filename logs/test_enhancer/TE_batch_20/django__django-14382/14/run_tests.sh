#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.test_startapp_target_current_dir_explicit_path_dot admin_scripts.tests_llm.test_startapp_target_dot admin_scripts.tests_llm.test_startapp_target_dot_multiple_trailing_slashes admin_scripts.tests_llm.test_startapp_target_dot_trailing_slash admin_scripts.tests_llm.test_startapp_target_dot_with_verbose_flag admin_scripts.tests_llm.test_startapp_target_single_dot_string_multiple_forms admin_scripts.tests_llm.test_startapp_target_tilde admin_scripts.tests_llm.test_startapp_target_tilde_and_dot_combo admin_scripts.tests_llm.test_startapp_target_tilde_as_home_directory_name_being_identifier admin_scripts.tests_llm.test_startapp_target_tilde_with_trailing_slash
coverage json -o coverage.json
: '>>>>> End Test Output'
