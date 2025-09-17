#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ProgramNameRegressionTests.test_execute_from_command_line_usage_shows_empty_prog_for_empty_argv0 admin_scripts.tests_llm.ProgramNameRegressionTests.test_execute_from_command_line_with_none_argv0_raises_type_error admin_scripts.tests_llm.ProgramNameRegressionTests.test_init_with_none_argv0_raises_type_error admin_scripts.tests_llm.ProgramNameRegressionTests.test_main_help_text_includes_empty_prog_name_when_argv0_empty_string admin_scripts.tests_llm.ProgramNameRegressionTests.test_management_utility_execute_prints_main_help_with_empty_prog admin_scripts.tests_llm.ProgramNameRegressionTests.test_management_utility_execute_with_none_argv0_raises_type_error admin_scripts.tests_llm.ProgramNameRegressionTests.test_prog_name_is_empty_string_when_argv0_is_empty_string
coverage json -o coverage.json
: '>>>>> End Test Output'
