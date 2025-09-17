#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.StartAppDots.test_dot_and_trailing_slashes_combination admin_scripts.tests_llm.StartAppDots.test_dot_prefix_with_extra_slashes admin_scripts.tests_llm.StartAppDots.test_dot_with_current_dir_component_only admin_scripts.tests_llm.StartAppDots.test_dot_with_redundant_components admin_scripts.tests_llm.StartAppDots.test_dot_with_trailing_dotslash_sequence admin_scripts.tests_llm.StartAppDots.test_multiple_dot_segments_in_target_app_directory_name admin_scripts.tests_llm.StartAppDots.test_multiple_mixed_dot_and_empty_components admin_scripts.tests_llm.StartAppDots.test_trailing_dot_in_target_app_directory_name admin_scripts.tests_llm.StartAppDots.test_trailing_dot_slash_in_target_app_directory_name admin_scripts.tests_llm.StartAppDots.test_trailing_dot_using_relative_parent_components
coverage json -o coverage.json
: '>>>>> End Test Output'
