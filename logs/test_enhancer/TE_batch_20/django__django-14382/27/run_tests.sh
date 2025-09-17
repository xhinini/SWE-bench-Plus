#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.StartAppDotPathVariants._run_variant admin_scripts.tests_llm.StartAppDotPathVariants.test_absolute_path_with_trailing_dot admin_scripts.tests_llm.StartAppDotPathVariants.test_complex_mixed_dot_segments admin_scripts.tests_llm.StartAppDotPathVariants.test_dot_slash_sequence admin_scripts.tests_llm.StartAppDotPathVariants.test_double_current_dir_in_path admin_scripts.tests_llm.StartAppDotPathVariants.test_leading_dot_relative_path admin_scripts.tests_llm.StartAppDotPathVariants.test_mixed_dot_parent_references admin_scripts.tests_llm.StartAppDotPathVariants.test_relative_with_dot_and_current_dir_prefix admin_scripts.tests_llm.StartAppDotPathVariants.test_relative_with_dot_and_sep admin_scripts.tests_llm.StartAppDotPathVariants.test_relative_with_multiple_dot_segments admin_scripts.tests_llm.StartAppDotPathVariants.test_relative_with_trailing_dot
coverage json -o coverage.json
: '>>>>> End Test Output'
