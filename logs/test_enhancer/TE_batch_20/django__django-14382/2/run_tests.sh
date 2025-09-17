#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.StartAppDotTests._run_and_assert_created admin_scripts.tests_llm.StartAppDotTests.test_absolute_target_ending_with_dot admin_scripts.tests_llm.StartAppDotTests.test_absolute_target_with_dot_and_trailing_slash admin_scripts.tests_llm.StartAppDotTests.test_absolute_target_with_parent_dotdot_segment admin_scripts.tests_llm.StartAppDotTests.test_complex_dot_segments admin_scripts.tests_llm.StartAppDotTests.test_target_ending_with_dot admin_scripts.tests_llm.StartAppDotTests.test_target_ending_with_dot_and_trailing_slash admin_scripts.tests_llm.StartAppDotTests.test_target_prefixed_with_dot_and_ending_dot admin_scripts.tests_llm.StartAppDotTests.test_target_with_multiple_dot_segments admin_scripts.tests_llm.StartAppDotTests.test_target_with_parent_dotdot_segment admin_scripts.tests_llm.StartAppDotTests.test_target_with_trailing_parent_and_slash
coverage json -o coverage.json
: '>>>>> End Test Output'
