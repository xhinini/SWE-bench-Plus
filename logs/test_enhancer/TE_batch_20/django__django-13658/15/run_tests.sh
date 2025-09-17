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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_argv0_false_raises_typeerror admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_argv0_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_argv0_zero_raises_typeerror admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_empty_string_sets_empty_prog_name admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_execute_from_command_line_uses_passed_argv_program_name admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_execute_from_command_line_with_none_argv0_raises_typeerror admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_main_help_text_includes_empty_progname admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_program_name_retained_for_paths_with_extension
coverage json -o coverage.json
: '>>>>> End Test Output'
