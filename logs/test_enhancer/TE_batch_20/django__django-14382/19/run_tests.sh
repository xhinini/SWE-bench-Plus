#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.test_target_with_current_segment_absolute admin_scripts.tests_llm.test_target_with_current_segment_absolute_trailing_slash admin_scripts.tests_llm.test_target_with_current_segment_dot_prefix admin_scripts.tests_llm.test_target_with_current_segment_relative admin_scripts.tests_llm.test_target_with_current_segment_relative_trailing_slash admin_scripts.tests_llm.test_target_with_parent_segment_absolute admin_scripts.tests_llm.test_target_with_parent_segment_absolute_trailing_slash admin_scripts.tests_llm.test_target_with_parent_segment_dot_prefix admin_scripts.tests_llm.test_target_with_parent_segment_relative admin_scripts.tests_llm.test_target_with_parent_segment_relative_trailing_slash
coverage json -o coverage.json
: '>>>>> End Test Output'
