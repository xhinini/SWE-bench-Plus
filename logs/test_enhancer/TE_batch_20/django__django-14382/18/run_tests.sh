#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.StartAppTrailingDotTests.test_trailing_dot_absolute admin_scripts.tests_llm.StartAppTrailingDotTests.test_trailing_dot_absolute_parent_refs admin_scripts.tests_llm.StartAppTrailingDotTests.test_trailing_dot_absolute_with_multiple_dots admin_scripts.tests_llm.StartAppTrailingDotTests.test_trailing_dot_absolute_with_slash admin_scripts.tests_llm.StartAppTrailingDotTests.test_trailing_dot_relative admin_scripts.tests_llm.StartAppTrailingDotTests.test_trailing_dot_relative_nested admin_scripts.tests_llm.StartAppTrailingDotTests.test_trailing_dot_relative_nested_with_slash admin_scripts.tests_llm.StartAppTrailingDotTests.test_trailing_dot_relative_with_slash admin_scripts.tests_llm.StartAppTrailingDotTests.test_trailing_dot_with_parent_refs_relative
coverage json -o coverage.json
: '>>>>> End Test Output'
