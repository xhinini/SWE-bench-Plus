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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ProgramNameHelpTests.test_command_flag_help_shows_usage_with_empty_prog admin_scripts.tests_llm.ProgramNameHelpTests.test_help_for_specific_command_via_help_subcommand_contains_empty_prog admin_scripts.tests_llm.ProgramNameHelpTests.test_help_subcommand_shows_per_command_usage_with_empty_prog admin_scripts.tests_llm.ProgramNameHelpTests.test_help_text_contains_available_subcommands_and_empty_prog admin_scripts.tests_llm.ProgramNameHelpTests.test_help_uses_empty_argv0_program_name admin_scripts.tests_llm.ProgramNameHelpTests.test_long_help_flag_uses_empty_argv0_program_name admin_scripts.tests_llm.ProgramNameHelpTests.test_short_help_flag_uses_empty_argv0_program_name admin_scripts.tests_llm.ProgramNameHelpTests.test_specific_command_help_via_run_from_argv_uses_empty_prog
coverage json -o coverage.json
: '>>>>> End Test Output'
