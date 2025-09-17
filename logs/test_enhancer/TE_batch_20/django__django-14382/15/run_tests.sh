#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.TemplateTargetBasenameTests.test_target_abs_path_ending_with_dot admin_scripts.tests_llm.TemplateTargetBasenameTests.test_target_abs_path_with_dot_dot admin_scripts.tests_llm.TemplateTargetBasenameTests.test_target_ends_with_dot admin_scripts.tests_llm.TemplateTargetBasenameTests.test_target_ends_with_dot_and_trailing_slash admin_scripts.tests_llm.TemplateTargetBasenameTests.test_target_with_complex_dot_patterns admin_scripts.tests_llm.TemplateTargetBasenameTests.test_target_with_dot_dot_and_trailing_slash admin_scripts.tests_llm.TemplateTargetBasenameTests.test_target_with_dot_dot_segment admin_scripts.tests_llm.TemplateTargetBasenameTests.test_target_with_double_slash_and_dot admin_scripts.tests_llm.TemplateTargetBasenameTests.test_target_with_leading_dot_component admin_scripts.tests_llm.TemplateTargetBasenameTests.test_target_with_multiple_dot_segments
coverage json -o coverage.json
: '>>>>> End Test Output'
