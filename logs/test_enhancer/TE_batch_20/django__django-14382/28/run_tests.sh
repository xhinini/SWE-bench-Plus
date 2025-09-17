#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.StartAppPathNormalization._assert_startapp_creates admin_scripts.tests_llm.StartAppPathNormalization._make_app_dir admin_scripts.tests_llm.StartAppPathNormalization.test_absolute_with_dot_and_normalization admin_scripts.tests_llm.StartAppPathNormalization.test_mixed_dot_and_parent_segments admin_scripts.tests_llm.StartAppPathNormalization.test_tilde_expansion_with_trailing_dot admin_scripts.tests_llm.StartAppPathNormalization.test_trailing_dot_absolute admin_scripts.tests_llm.StartAppPathNormalization.test_trailing_dot_double_slash admin_scripts.tests_llm.StartAppPathNormalization.test_trailing_dot_relative admin_scripts.tests_llm.StartAppPathNormalization.test_trailing_dot_with_extra_separators admin_scripts.tests_llm.StartAppPathNormalization.test_trailing_multiple_dots_segments admin_scripts.tests_llm.StartAppPathNormalization.test_trailing_parent_absolute admin_scripts.tests_llm.StartAppPathNormalization.test_trailing_parent_relative
coverage json -o coverage.json
: '>>>>> End Test Output'
