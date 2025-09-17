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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ProgramNameEmptyTests.test_execute_from_command_line_dash_h_uses_empty_prog admin_scripts.tests_llm.ProgramNameEmptyTests.test_execute_from_command_line_double_dash_help_uses_empty_prog admin_scripts.tests_llm.ProgramNameEmptyTests.test_execute_from_command_line_help_commands_flag_uses_empty_prog_for_general_help admin_scripts.tests_llm.ProgramNameEmptyTests.test_execute_from_command_line_help_short_and_long_show_empty_prog admin_scripts.tests_llm.ProgramNameEmptyTests.test_execute_from_command_line_help_uses_argv_progname_empty admin_scripts.tests_llm.ProgramNameEmptyTests.test_fetch_command_unknown_writes_progname_empty_to_stderr admin_scripts.tests_llm.ProgramNameEmptyTests.test_help_for_subcommand_prints_usage_with_empty_prog admin_scripts.tests_llm.ProgramNameEmptyTests.test_main_help_text_progname_empty admin_scripts.tests_llm.ProgramNameEmptyTests.test_management_utility_prog_name_property_empty admin_scripts.tests_llm.ProgramNameEmptyTests.test_specific_help_usage_shows_empty_prog
coverage json -o coverage.json
: '>>>>> End Test Output'
