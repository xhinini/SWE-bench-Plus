#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.StartAppPathNormalization._run_startapp_and_assert admin_scripts.tests_llm.StartAppPathNormalization.setUp admin_scripts.tests_llm.StartAppPathNormalization.test_target_is_dot_slash admin_scripts.tests_llm.StartAppPathNormalization.test_target_is_parent_dotdot admin_scripts.tests_llm.StartAppPathNormalization.test_target_is_single_dot admin_scripts.tests_llm.StartAppPathNormalization.test_target_with_complex_dot_dot_and_dot admin_scripts.tests_llm.StartAppPathNormalization.test_target_with_dot_slash_trailing admin_scripts.tests_llm.StartAppPathNormalization.test_target_with_parent_ref admin_scripts.tests_llm.StartAppPathNormalization.test_target_with_parent_ref_trailing_slash admin_scripts.tests_llm.StartAppPathNormalization.test_target_with_redundant_slashes_and_dot admin_scripts.tests_llm.StartAppPathNormalization.test_target_with_single_dot_component
coverage json -o coverage.json
: '>>>>> End Test Output'
